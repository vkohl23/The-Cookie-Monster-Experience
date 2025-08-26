import streamlit as st
from PIL import Image
import random

st.set_page_config(layout="wide")
st.title("CookieMonster")

player_img = Image.open("boy.png").resize((40, 40))
cookie_img = Image.open("cookie.jpg").resize((25, 25))
broccoli_img = Image.open("broccoli.png").resize((30, 30))

GRID_SIZE = 10  
CELL_SIZE = 50


if "player_pos" not in st.session_state:
    st.session_state.player_pos = [GRID_SIZE // 2, GRID_SIZE // 2]
if "cookies" not in st.session_state:
    st.session_state.cookies = [[random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)] for _ in range(15)]
if "broccolis" not in st.session_state:
    st.session_state.broccolis = [[random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)] for _ in range(5)]
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False


def move_player(direction):
    if st.session_state.game_over:
        return
    x, y = st.session_state.player_pos
    if direction == "Up": y -= 1
    elif direction == "Down": y += 1
    elif direction == "Left": x -= 1
    elif direction == "Right": x += 1

  
    x = max(0, min(GRID_SIZE-1, x))
    y = max(0, min(GRID_SIZE-1, y))
    st.session_state.player_pos = [x, y]

    # Eat cookie
    if [x, y] in st.session_state.cookies:
        st.session_state.cookies.remove([x, y])
        st.session_state.score += 1

    
    new_broccolis = []
    for bx, by in st.session_state.broccolis:
        if bx < x: bx += 1
        elif bx > x: bx -= 1
        if by < y: by += 1
        elif by > y: by -= 1
        new_broccolis.append([bx, by])
    st.session_state.broccolis = new_broccolis

  
    if [x, y] in st.session_state.broccolis:
        st.session_state.game_over = True

cols = st.columns(3)
with cols[0]:
    if st.button("Up"):
        move_player("Up")
with cols[1]:
    if st.button("Left"):
        move_player("Left")
    if st.button("Right"):
        move_player("Right")
with cols[2]:
    if st.button("Down"):
        move_player("Down")


for y in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for x in range(GRID_SIZE):
        cell_img = Image.new("RGB", (CELL_SIZE, CELL_SIZE), color=(0,0,0))
        if [x, y] == st.session_state.player_pos:
            cell_img.paste(player_img, ((CELL_SIZE - player_img.width)//2, (CELL_SIZE - player_img.height)//2))
        elif [x, y] in st.session_state.cookies:
            cell_img.paste(cookie_img, ((CELL_SIZE - cookie_img.width)//2, (CELL_SIZE - cookie_img.height)//2))
        elif [x, y] in st.session_state.broccolis:
            cell_img.paste(broccoli_img, ((CELL_SIZE - broccoli_img.width)//2, (CELL_SIZE - broccoli_img.height)//2))
        cols[x].image(cell_img)


st.markdown(f"**Score:** {st.session_state.score}")
if st.session_state.game_over:
    st.markdown("**Game Over!** Refresh to play again.")

