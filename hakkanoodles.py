import streamlit as st

# Sample user data
profiles = [
    {"name": "Alice", "img": "https://i.imgur.com/ExdKOOz.png"},
    {"name": "Bob", "img": "https://i.imgur.com/ExdKOOz.png"},
    {"name": "Charlie", "img": "https://i.imgur.com/ExdKOOz.png"}
]

if "index" not in st.session_state:
    st.session_state.index = 0

def swipe(direction):
    profile = profiles[st.session_state.index]
    st.write(f"You swiped {direction} on {profile['name']}")
    st.session_state.index += 1

if st.session_state.index < len(profiles):
    person = profiles[st.session_state.index]
    st.image(person["img"], width=300)
    st.subheader(person["name"])
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Swipe Left"):
            swipe("left")
    with col2:
        if st.button("❤ Swipe Right"):
            swipe("right")
else:
    st.write("No more profiles!")