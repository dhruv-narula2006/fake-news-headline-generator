import streamlit as st
import random
from datetime import datetime

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Fake News Generator", page_icon="📰", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main-title {
    font-size: 42px;
    text-align: center;
    color: #ff4b4b;
    font-weight: bold;
}
.headline-box {
    padding: 20px;
    border-radius: 10px;
    font-size: 24px;
    text-align: center;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📰 Fake News Headline Generator</p>', unsafe_allow_html=True)

# ------------------ DEFAULT DATA ------------------
default_subjects = ["Shahrukh Khan", "Virat Kohli", "Prime Minister Modi"]
default_actions = ["launches", "cancels", "celebrates"]
default_objects = ["new movie", "cricket tournament", "national policy"]
default_places = ["at Red Fort", "in Mumbai", "at India Gate"]

# ------------------ FUNCTIONS ------------------
def parse_input(text, default):
    if text.strip() == "":
        return default
    return [x.strip() for x in text.split(",") if x.strip()]

def grammar_fix(subject, action, obj, place):
    if not subject.lower().endswith("s") and not action.endswith("s"):
        action += "s"

    if not obj.startswith(("a ", "an ", "the ")):
        obj = ("an " if obj[0].lower() in "aeiou" else "a ") + obj

    if not place.startswith(("at ", "in ", "on ")):
        place = "at " + place

    return f"BREAKING NEWS: {subject} {action} {obj} {place}!"

# ------------------ SIDEBAR ------------------
st.sidebar.header("⚙️ Settings")

mode = st.sidebar.selectbox("Mode", ["Funny", "Serious"])
save_option = st.sidebar.checkbox("Save Headlines")

# ------------------ INPUT AREA ------------------
col1, col2 = st.columns(2)

with col1:
    subjects_input = st.text_input("Subjects")
    actions_input = st.text_input("Actions")

with col2:
    objects_input = st.text_input("Objects")
    places_input = st.text_input("Places")

subjects = parse_input(subjects_input, default_subjects)
actions = parse_input(actions_input, default_actions)
objects = parse_input(objects_input, default_objects)
places = parse_input(places_input, default_places)

# ------------------ SESSION STATE ------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ GENERATE BUTTON ------------------
if st.button("🚀 Generate Headline"):
    subject = random.choice(subjects)
    action = random.choice(actions)
    obj = random.choice(objects)
    place = random.choice(places)

    headline = grammar_fix(subject, action, obj, place)

    st.markdown(f'<div class="headline-box">{headline}</div>', unsafe_allow_html=True)

    if save_option:
        st.session_state.history.append(
            f"[{datetime.now().strftime('%H:%M:%S')}] {headline}"
        )

# ------------------ HISTORY ------------------
if st.session_state.history:
    st.subheader("📂 Saved Headlines")
    for h in st.session_state.history:
        st.write(h)

    st.download_button(
        "⬇ Download Headlines",
        "\n".join(st.session_state.history),
        file_name="headlines.txt"
    )