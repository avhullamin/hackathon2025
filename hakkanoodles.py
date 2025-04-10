import streamlit as st
import mysql.connector
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Database setup (runs once to create and populate)
def initialize_database():
    print("Initializing database...")
    conn = mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        database="sql12772267",
        user="sql12772267",
        password="DivGzu7cSP",
        port=3306
    )
    cursor = conn.cursor()
    
    print("Creating table if not exists...")
    cursor.execute('''CREATE TABLE IF NOT EXISTS student_details (
        USN VARCHAR(10) PRIMARY KEY,
        NAME TEXT,
        EMAIL TEXT,
        BRANCH TEXT,
        SEM INTEGER,
        DBMS INTEGER,
        DSA INTEGER,
        MATHS INTEGER,
        PYTHON INTEGER,
        PREF TEXT
    )''')
    
    print("Checking if table is empty...")
    cursor.execute("SELECT COUNT(*) FROM student_details")
    if cursor.fetchone()[0] == 0:
        print("Populating sample data...")
        sample_data = [
            ('1SG23CS001', 'A R Sagar', 'a.r.sagar808@gmail.com', 'CS', 3, 54, 77, 25, 95, 'DBMS'),
            ('1SG23CS002', 'Aaryan Kumar', 'aaryan1203@gmail.com', 'CS', 1, 13, 68, 3, 8, 'DSA'),
            ('1SG23CS003', 'Abhay Raj', 'rajabhay9534@gmail.com', 'CS', 3, 42, 12, 35, 40, 'MATHS'),
            ('1SG23CS004', 'Abhishek Saini', 'abhisheksaini5656000@gmail.com', 'CS', 8, 45, 47, 2, 70, 'PYTHON'),
            ('1SG23CS005', 'Aditya P', 'adityaq0p@gmail.com', 'CS', 4, 14, 35, 34, 65, 'DBMS'),
            ('1SG23CS006', 'Ajay Jayaram', 'Ajajayaram01@gmail.com', 'CS', 3, 30, 77, 92, 33, 'DSA'),
            ('1SG23CS007', 'Akash S Mulki Gowda', 'akashmulkigowda@gmail.com', 'CS', 8, 47, 69, 4, 14, 'MATHS'),
            ('1SG23CS008', 'Akshath V Nadig', 'akshathvnadig@gmail.com', 'CS', 5, 49, 73, 18, 71, 'PYTHON'),
            ('1SG23CS009', 'Akshatha S', 'keerthiakshatha@gmail.com', 'CS', 2, 2, 3, 9, 0, 'DBMS'),
            ('1SG23CS010', 'Ambika', 'nagarathnanagu6195@gmail.com', 'CS', 4, 61, 94, 89, 60, 'DSA'),
            ('1SG23CS011', 'Anjali Singh', 'anjalisinghmath@gmail.com', 'CS', 3, 3, 3, 8, 33, 'MATHS'),
            ('1SG23CS012', 'Ankith V Hullamani', 'ankithv0027@gmail.com', 'CS', 4, 9, 23, 85, 59, 'PYTHON'),
            ('1SG23CS013', 'Anusha S A', 'anushasa79@gmail.com', 'CS', 4, 14, 58, 47, 60, 'DBMS'),
            ('1SG23CS014', 'Anushree U', 'anushreeu92@gmail.com', 'CS', 6, 30, 64, 29, 55, 'DSA'),
            ('1SG23CS015', 'Apoorva G R', 'apoorvagr10@gmail.com', 'CS', 8, 83, 47, 86, 91, 'MATHS'),
            ('1SG23CS016', 'Arnav Singh Thapa', 'arnavthapa95@gmail.com', 'CS', 8, 8, 51, 34, 15, 'PYTHON'),
            ('1SG23CS017', 'Arun Kumar A R', 'arunkumarar58@gmail.com', 'CS', 6, 24, 0, 28, 42, 'DBMS'),
            ('1SG23CS018', 'Ashish G Shetty', 'ashishgs1604@gmail.com', 'CS', 3, 2, 35, 67, 33, 'DSA'),
            ('1SG23CS019', 'Ashish Kumar', 'ashish9430kr@gmail.com', 'CS', 6, 10, 4, 65, 15, 'MATHS')
        ]
        cursor.executemany('INSERT INTO student_details (USN, NAME, EMAIL, BRANCH, SEM, DBMS, DSA, MATHS, PYTHON, PREF) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', sample_data)
    
    conn.commit()
    print("Database initialized and committed.")
    conn.close()

# Generate OTP
def generate_otp():
    otp = str(random.randint(100000, 999999))
    print(f"Generated OTP: {otp}")
    return otp

# Send OTP via Gmail SMTP
def send_otp_email(email, otp):
    sender_email = "unisap.library.app@gmail.com"  # Replace with your Gmail address
    app_password = "lndw uocy nshz vqfn"  # Replace with your App Password
    
    print(f"Attempting to send OTP to {email}...")
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Your OTP for Match App"
    body = f"Your OTP is {otp}. It is valid for 5 minutes."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print(f"OTP sent successfully to {email}")
        return True
    except Exception as e:
        print(f"Failed to send OTP: {str(e)}")
        st.error(f"Failed to send OTP: {str(e)}")
        return False

# Matching logic
def calculate_match_score(user1, user2):
    score = 0
    if user1[3] == user2[3]:  # Branch match
        score += 40
    if abs(user1[4] - user2[4]) <= 1:  # Semester closeness
        score += 30
    avg1 = (user1[5] + user1[6] + user1[7] + user1[8]) / 4
    avg2 = (user2[5] + user2[6] + user2[7] + user2[8]) / 4
    if abs(avg1 - avg2) <= 10:  # Marks closeness (average)
        score += 20
    if user1[9] == user2[9]:  # Preferences match
        score += 10
    return score

# Main app function
def main_app():
    print("Entering main_app function...")
    conn = mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        database="sql12772267",
        user="sql12772267",
        password="DivGzu7cSP",
        port=3306
    )
    cursor = conn.cursor()
    cursor.execute("SELECT USN, NAME FROM student_details")
    users = cursor.fetchall()
    user_dict = {name: usn for usn, name in users}

    print(f"Logged-in user USN: {st.session_state.user_usn}")
    selected_user = [name for _, name in users if _ == st.session_state.user_usn][0]
    user_usn = st.session_state.user_usn

    print(f"Fetching data for user: {user_usn}")
    cursor.execute("SELECT * FROM student_details WHERE USN = %s", (user_usn,))
    current_user = cursor.fetchone()

    print("Displaying user profile...")
    st.subheader("Your Profile")
    st.write(f"Branch: {current_user[3]}")
    st.write(f"Semester: {current_user[4]}")
    st.write(f"Average Marks: {round((current_user[5] + current_user[6] + current_user[7] + current_user[8]) / 4, 2)}")
    st.write(f"Preferences: {current_user[9]}")

    print("Finding matches...")
    cursor.execute("SELECT * FROM student_details WHERE USN != %s", (user_usn,))
    all_users = cursor.fetchall()
    conn.close()

    matches = []
    for other_user in all_users:
        score = calculate_match_score(current_user, other_user)
        if score >= 70:
            matches.append((other_user[1], score, other_user[3], other_user[4], round((other_user[5] + other_user[6] + other_user[7] + other_user[8]) / 4, 2), other_user[9]))

    print(f"Found {len(matches)} matches.")
    matches.sort(key=lambda x: x[1], reverse=True)

    if matches:
        if 'match_index' not in st.session_state:
            st.session_state.match_index = 0
            print("Initialized match_index to 0")
        if 'liked' not in st.session_state:
            st.session_state.liked = []
            print("Initialized liked list")

        current_match = matches[st.session_state.match_index]
        print(f"Displaying match: {current_match[0]} with score {current_match[1]}%")
        st.subheader("Swipe Time!")
        st.write(f"**Name**: {current_match[0]}")
        st.write(f"Branch: {current_match[2]}")
        st.write(f"Semester: {current_match[3]}")
        st.write(f"Average Marks: {current_match[4]}")
        st.write(f"Preferences: {current_match[5]}")
        st.write(f"Match Score: {current_match[1]}%")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Nope 👎"):
                print("Nope button clicked")
                if st.session_state.match_index < len(matches) - 1:
                    st.session_state.match_index += 1
                    print(f"Incremented match_index to {st.session_state.match_index}")
                else:
                    print("No more matches")
                    st.write("No more matches!")
        with col2:
            if st.button("Like 👍"):
                print("Like button clicked")
                st.session_state.liked.append(current_match[0])
                print(f"Added {current_match[0]} to liked list")
                if st.session_state.match_index < len(matches) - 1:
                    st.session_state.match_index += 1
                    print(f"Incremented match_index to {st.session_state.match_index}")
                else:
                    print("No more matches")
                    st.write("No more matches!")

        if st.session_state.liked:
            print(f"Displaying {len(st.session_state.liked)} liked matches")
            st.subheader("Your Likes")
            for liked_name in st.session_state.liked:
                st.write(f"- {liked_name}")
    else:
        print("No matches found")
        st.write("No matches found!")

# Callback function for OTP verification
def verify_otp():
    print(f"Verify OTP button clicked with input: {st.session_state.otp_input}")
    if st.session_state.otp_input == st.session_state.generated_otp:
        print("OTP verified successfully")
        st.session_state.logged_in = True
        st.session_state.user_usn = st.session_state.usn  # Use the USN from the input
        print(f"Setting logged_in to True and user_usn to {st.session_state.usn}")
    else:
        print("OTP verification failed")
        st.error("Invalid OTP. Please try again.")

# Main application flow
st.title("Match App Login 🎉")

print(f"Session state at start: {st.session_state}")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_usn = None
    st.session_state.otp = None
    st.session_state.generated_otp = None
    st.session_state.otp_input = ""
    st.session_state.usn = None  # Store USN temporarily
    print("Initialized session state with default values")

# Login page using a form to ensure proper rendering
if not st.session_state.logged_in:
    print("Displaying login page...")
    with st.form(key="login_form"):
        st.subheader("Login")
        usn = st.text_input("Enter your USN:")
        submit_button = st.form_submit_button("Generate OTP")
        if submit_button:
            print(f"Generate OTP button clicked for USN: {usn}")
            if usn:
                conn = mysql.connector.connect(
                    host="sql12.freesqldatabase.com",
                    database="sql12772267",
                    user="sql12772267",
                    password="DivGzu7cSP",
                    port=3306
                )
                cursor = conn.cursor()
                cursor.execute("SELECT EMAIL FROM student_details WHERE USN = %s", (usn,))
                result = cursor.fetchone()
                conn.close()
                if result:
                    email = result[0]
                    print(f"Found email: {email} for USN {usn}")
                    otp = generate_otp()
                    st.session_state.generated_otp = otp
                    st.session_state.usn = usn  # Store USN in session state
                    if send_otp_email(email, otp):
                        print(f"OTP {otp} sent successfully")
                        st.success(f"OTP sent to {email}. Please check your inbox (and spam folder).")
                    else:
                        print("Failed to send OTP")
                        st.error("Failed to send OTP. Please try again later.")
                else:
                    print(f"USN {usn} not found in database")
                    st.error("USN not found in the database.")
            else:
                print("No USN entered")
                st.error("Please enter a USN.")

    # OTP verification section
    if st.session_state.generated_otp:
        otp_input = st.text_input("Enter OTP:", key="otp_input")
        if st.button("Verify OTP", on_click=verify_otp):
            pass  # Callback handles the logic

# Main app after login
else:
    print("User is logged in, calling main_app...")
    main_app()