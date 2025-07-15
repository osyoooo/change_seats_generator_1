# seat_generator_app.py
import streamlit as st
import pandas as pd
import random

st.title("🎯 席替えジェネレーター（教室設定 → CSV読み込み → 席提案）")

# 1. 教室の机の配置設定
st.sidebar.header("🪑 教室レイアウト設定")
rows = st.sidebar.number_input("行数（前から後ろ）", min_value=1, max_value=20, value=4)
cols = st.sidebar.number_input("列数（左から右）", min_value=1, max_value=20, value=3)

seat_positions = [(r, c) for r in range(rows) for c in range(cols)]

# 2. CSVファイルのアップロード
tudents = []
st.subheader("📄 生徒情報のCSVアップロード")
uploaded_file = st.file_uploader("生徒情報CSVをアップロードしてください（出席番号, 性別, 配慮事項）", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    for _, row in df.iterrows():
        student = {
            "id": int(row["出席番号"]),
            "gender": row["性別"],
            "special": row["配慮事項"].split("/") if pd.notna(row["配慮事項"]) else []
        }
        students.append(student)
else:
    st.warning("⚠️ CSVファイルをアップロードしてください")
    st.stop()

# 3. 相性による分離ルールの指定
st.subheader("🚫 相性による分離ルール")
separation_pairs = []
num_students = len(students)
num_separations = st.number_input("分離ペアの数を入力", 0, 20, 0)

for i in range(num_separations):
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input(f"ペア{i+1}：生徒Aの出席番号", 1, num_students, key=f"sep_a_{i}")
    with col2:
        b = st.number_input(f"ペア{i+1}：生徒Bの出席番号", 1, num_students, key=f"sep_b_{i}")
    if a != b:
        separation_pairs.append((a, b))

# 4. 配慮ロジックの定義
def is_front_preferred(student):
    return "視力" in student["special"]

def is_back_preferred(student):
    return "身長" in student["special"]

# 5. 座席割り当て
st.subheader("✨ 席替え提案結果")
random.shuffle(seat_positions)
assigned = {}
used = set()

for student in students:
    preferred = []
    for pos in seat_positions:
        if pos in used:
            continue
        if is_front_preferred(student) and pos[0] > rows // 2:
            continue
        if is_back_preferred(student) and pos[0] < rows // 2:
            continue
        preferred.append(pos)

    seat = preferred[0] if preferred else [p for p in seat_positions if p not in used][0]
    assigned[student["id"]] = seat
    used.add(seat)

# 6. 分離ルールチェック
warnings = []
for a, b in separation_pairs:
    if a in assigned and b in assigned:
        ra, ca = assigned[a]
        rb, cb = assigned[b]
        if abs(ra - rb) <= 1 and abs(ca - cb) <= 1:
            warnings.append(f"⚠️ {a}番と{b}番が近すぎます（{(ra, ca)} ↔ {(rb, cb)}）")

# 7. 座席表示
seat_grid = [["" for _ in range(cols)] for _ in range(rows)]
for sid, (r, c) in assigned.items():
    gender = next(s["gender"] for s in students if s["id"] == sid)
    mark = "🧑‍🎓" if gender == "M" else "👩‍🎓"
    seat_grid[r][c] = f"{mark}{sid}"

for row in seat_grid:
    cols_ = st.columns(cols)
    for i, cell in enumerate(row):
        with cols_[i]:
            st.markdown(cell or "　")

# 8. 結果の警告表示
if warnings:
    st.warning("\n".join(warnings))
else:
    st.success("✅ 分離ルールはすべて守られました")
