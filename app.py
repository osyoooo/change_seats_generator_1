# app.py
import streamlit as st
import pandas as pd
import random

st.title("🎯 席替えジェネレーター（簡易版）")

# 1. 出席番号と性別の入力（簡易フォーム）
st.subheader("👥 生徒情報の入力")
students = []
num_students = st.number_input("生徒数を入力してください", 1, 40, 10)

for i in range(1, num_students + 1):
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox(f"{i}番 性別", ["M", "F"], key=f"gender_{i}")
    with col2:
        special = st.multiselect(f"{i}番 配慮事項", ["視力", "身長", "聴力"], key=f"special_{i}")
    students.append({"id": i, "gender": gender, "special": special})

# 2. 配慮ロジックの定義（超簡易）
def is_front_preferred(student):
    return "視力" in student["special"]

def is_back_preferred(student):
    return "身長" in student["special"]

# 3. 座席割り当て（3列×4行 = 12席）
st.subheader("🪑 座席割り当て結果")
rows, cols = 4, 3
seat_positions = [(r, c) for r in range(rows) for c in range(cols)]
random.shuffle(seat_positions)

assigned = {}
used = set()

for student in students:
    preferred = []
    for pos in seat_positions:
        if pos in used:
            continue
        if is_front_preferred(student) and pos[0] > 1:
            continue
        if is_back_preferred(student) and pos[0] < 2:
            continue
        preferred.append(pos)

    seat = preferred[0] if preferred else [p for p in seat_positions if p not in used][0]
    assigned[student["id"]] = seat
    used.add(seat)

# 座席表示
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
