import streamlit as st
import sqlite3

# Database setup (runs once to create and populate)
def initialize_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        branch TEXT,
        semester INTEGER,
        gpa REAL,
        marks_sub1 INTEGER,
        marks_sub2 INTEGER,
        marks_sub3 INTEGER,
        marks_sub4 INTEGER,
        preferences TEXT
    )''')
    
    # Sample data (only inserts if table is empty)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            (1, 'Alice', 'CS', 3, 3.8, 85, 90, 70, 80, 'chat'),
            (2, 'Bob', 'CS', 4, 3.6, 80, 85, 75, 78, 'chat'),
            (3, 'Charlie', 'Mech', 3, 3.2, 70, 65, 80, 75, 'hangout'),
            (4, 'Dana', 'CS', 2, 3.9, 90, 88, 85, 82, 'chat'),
            (5, 'Eve', 'Mech', 4, 3.5, 78, 80, 70, 85, 'hangout')
        ]
        cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', sample_data)
    
    conn.commit()
    conn.close()

# Matching logic
def calculate_match_score(user1, user2):
    score = 0
    if user1[2] == user2[2]:  # Branch match
        score += 40
    if abs(user1[3] - user2[3]) <= 1:  # Semester closeness
        score += 30
    if abs(user1[4] - user2[4]) <= 0.5:  # GPA closeness
        score += 20
    if user1[9] == user2[9]:  # Preferences match
        score += 10
    return score

# Streamlit app
st.title("Match App 🎉")

# Initialize database
initialize_database()

# Connect to database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("SELECT id, name FROM users")
users = cursor.fetchall()
user_dict = {name: id for id, name in users}

# User selection
selected_user = st.selectbox("Choose yourself:", [name for _, name in users])
user_id = user_dict[selected_user]

# Get current user data
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
current_user = cursor.fetchone()

# Display user profile
st.subheader("Your Profile")
st.write(f"Branch: {current_user[2]}")
st.write(f"Semester: {current_user[3]}")
st.write(f"GPA: {current_user[4]}")
st.write(f"Preferences: {current_user[9]}")

# Find matches
cursor.execute("SELECT * FROM users WHERE id != ?", (user_id,))
all_users = cursor.fetchall()
conn.close()

matches = []
for other_user in all_users:
    score = calculate_match_score(current_user, other_user)
    if score >= 70:  # Threshold
        matches.append((other_user[1], score, other_user[2], other_user[3], other_user[4], other_user[9]))  # Name, score, branch, semester, gpa, preferences

# Sort matches by score
matches.sort(key=lambda x: x[1], reverse=True)

# Swipe UI using session state
if matches:
    # Initialize session state
    if 'match_index' not in st.session_state:
        st.session_state.match_index = 0
    if 'liked' not in st.session_state:
        st.session_state.liked = []

    # Display current match
    current_match = matches[st.session_state.match_index]
    st.subheader("Swipe Time!")
    st.write(f"**Name**: {current_match[0]}")
    st.write(f"Branch: {current_match[2]}")
    st.write(f"Semester: {current_match[3]}")
    st.write(f"GPA: {current_match[4]}")
    st.write(f"Preferences: {current_match[5]}")
    st.write(f"Match Score: {current_match[1]}%")

    # Swipe buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Nope 👎"):
            if st.session_state.match_index < len(matches) - 1:
                st.session_state.match_index += 1
            else:
                st.write("No more matches!")
    with col2:
        if st.button("Like 👍"):
            st.session_state.liked.append(current_match[0])
            if st.session_state.match_index < len(matches) - 1:
                st.session_state.match_index += 1
            else:
                st.write("No more matches!")

    # Show liked matches
    if st.session_state.liked:
        st.subheader("Your Likes")
        for liked_name in st.session_state.liked:
            st.write(f"- {liked_name}")
else:
    st.write("No matches found!")
