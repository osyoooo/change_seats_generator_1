# seat_generator_app.py

import streamlit as st
import pandas as pd

st.title("🎯 席替えジェネレーター（教室設定 → CSV読み込み → 条件付き席提案）")

# 1. 教室レイアウト設定
st.sidebar.header("🪑 教室レイアウト設定")
rows = st.sidebar.number_input("行数（前から後ろ）", min_value=1, max_value=20, value=4)
cols = st.sidebar.number_input("列数（左から右）", min_value=1, max_value=20, value=3)

# 前列優先：行番号（小さい順）→ 列番号（小さい順）でソート
seat_positions = sorted(
    [(r, c) for r in range(rows) for c in range(cols)],
    key=lambda pos: (pos[0], pos[1])
)

# 2. CSVファイルのアップロード
students = []
separation_pairs_csv = []

st.subheader("📄 生徒情報のCSVアップロード")
uploaded_file = st.file_uploader(
    "生徒情報CSVをアップロードしてください（出席番号, 性別, 配慮事項, 分離相手）",
    type="csv"
)

if not uploaded_file:
    st.warning("⚠️ まずはCSVファイルをアップロードしてください")
    st.stop()

df = pd.read_csv(uploaded_file)
for _, row in df.iterrows():
    sid = int(row["出席番号"])
    students.append({
        "id": sid,
        "gender": row["性別"],
        "special": row["配慮事項"].split("/") if pd.notna(row["配慮事項"]) else []
    })
    # CSVの「分離相手」も収集
    if "分離相手" in row and pd.notna(row["分離相手"]):
        try:
            partner = int(row["分離相手"])
            if partner != sid:
                separation_pairs_csv.append((sid, partner))
        except:
            pass

# 3. 席数チェック
if len(students) > len(seat_positions):
    st.error(f"❌ 生徒数（{len(students)}名）が座席数（{len(seat_positions)}席）を超えています。")
    st.stop()

# 4. UIでの手動分離ペア指定
st.subheader("🚫 分離ルール（CSV＋手動）")
separation_pairs_ui = []
num_seps = st.number_input("手動で追加する分離ペアの数", min_value=0, max_value=20, value=0)
for i in range(num_seps):
    a = st.number_input(f"ペア{i+1}：生徒Aの出席番号", 1, len(students), key=f"ui_a_{i}")
    b = st.number_input(f"ペア{i+1}：生徒Bの出席番号", 1, len(students), key=f"ui_b_{i}")
    if a != b:
        separation_pairs_ui.append((a, b))

# CSV由来＋UI入力を統合（重複排除）
separation_pairs = list(set(separation_pairs_csv + separation_pairs_ui))

# 5. 配慮・分離判定関数
def is_front_preferred(s): return "視力" in s["special"]
def is_back_preferred(s):  return "身長" in s["special"]
def is_too_close(p1, p2):
    return abs(p1[0] - p2[0]) <= 1 and abs(p1[1] - p2[1]) <= 1

# 6. 座席割り当て（前列優先＋自動分離考慮）
st.subheader("✨ 席替え提案結果")
assigned = {}
used = set()

for stu in students:
    # (A) 未使用席
    remaining = [p for p in seat_positions if p not in used]

    # (B) 配慮優先フィルタ
    preferred = [
        p for p in remaining
        if not (is_front_preferred(stu) and p[0] > rows // 2)
        and not (is_back_preferred(stu)  and p[0] < rows // 2)
    ]

    # (C) 分離ペアによる禁止席
    forbidden = set()
    for a, b in separation_pairs:
        # 自分がAで、相手Bが既に配置済みなら…
        if stu["id"] == a and b in assigned:
            forbidden |= {p for p in seat_positions if is_too_close(p, assigned[b])}
        # 自分がBで、相手Aが既に配置済みなら…
        if stu["id"] == b and a in assigned:
            forbidden |= {p for p in seat_positions if is_too_close(p, assigned[a])}

    # (D) 禁止席を除外
    preferred = [p for p in preferred  if p not in forbidden]
    remaining = [p for p in remaining if p not in forbidden]

    # (E) 席選択
    if preferred:
        seat = preferred[0]
    elif remaining:
        seat = remaining[0]
    else:
        st.error("❌ 配置可能な席がなくなりました。レイアウトか分離ルールを見直してください。")
        st.stop()

    assigned[stu["id"]] = seat
    used.add(seat)

# 7. 座席表示
seat_grid = [["　" for _ in range(cols)] for _ in range(rows)]
for sid, (r, c) in assigned.items():
    gender = next(s["gender"] for s in students if s["id"] == sid)
    icon = "👦" if gender == "M" else 👧"👧"
    seat_grid[r][c] = f"{icon}{sid}"

for row in seat_grid:
    cols_ = st.columns(cols)
    for i, cell in enumerate(row):
        with cols_[i]:
            st.markdown(cell)

# 8. 分離ペア再チェック（警告）
warnings = []
for a, b in separation_pairs:
    if a in assigned and b in assigned:
        if is_too_close(assigned[a], assigned[b]):
            warnings.append(f"⚠️ {a}番と{b}番が近すぎます（{assigned[a]} ↔ {assigned[b]}）")

if warnings:
    st.warning("\n".join(warnings))
else:
    st.success("✅ すべての条件が満たされました！")
