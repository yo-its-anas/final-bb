import streamlit as st
import pandas as pd
import geopy.distance as geopy_distance
from streamlit_lottie import st_lottie
import requests
import random
import string

# Function to load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_tfb3estd.json")

# Persistent User Storage (In-Memory for now)
users_db = {}

# Generate Random Username
def generate_username(name):
    return name.lower().replace(" ", "") + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

# Set page configuration
st.set_page_config(page_title="Karachi Blood Bank Finder", layout="wide")

# Adding custom CSS for fonts, colors, and more elegant UI
st.markdown("""
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f0f0;
        }
        .card {
            background-color: #ffffff;
            padding: 20px;
            margin: 10px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .card h3 {
            color: #1e90ff;
            font-size: 24px;
        }
        .card p {
            color: #333;
        }
        .header {
            text-align: center;
            color: #1e90ff;
            font-size: 36px;
            margin-top: 20px;
        }
        .icon {
            color: #1e90ff;
        }
        .button {
            background-color: #1e90ff;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
        }
        .button:hover {
            background-color: #4682b4;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for optional user authentication
st.sidebar.title("🔒 Optional User Authentication")
auth_option = st.sidebar.radio("Navigate", ["Sign In", "Sign Up", "Skip"])

if auth_option == "Sign Up":
    st.sidebar.header("Create Your Account")
    with st.sidebar.form("signup_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        password = st.text_input("Password", type="password")
        signup_submit = st.form_submit_button("Sign Up")

    if signup_submit:
        if email and password and name and blood_group:
            username = generate_username(name)
            if email in users_db:
                st.sidebar.error("📧 Email already registered!")
            else:
                users_db[email] = {"name": name, "username": username, "blood_group": blood_group, "password": password}
                st.sidebar.success(f"🎉 Account created! Your username is **{username}**")
        else:
            st.sidebar.error("❌ Please fill in all fields!")

elif auth_option == "Sign In":
    st.sidebar.header("Log In to Your Account")
    with st.sidebar.form("signin_form"):
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        signin_submit = st.form_submit_button("Sign In")

    if signin_submit:
        valid_user = any(user["username"] == username_input and user["password"] == password_input for user in users_db.values())
        if valid_user:
            st.session_state["logged_in_user"] = username_input
            st.sidebar.success(f"👋 Welcome back, {username_input}!")
            st.sidebar.button("Log Out", on_click=lambda: st.session_state.pop("logged_in_user"))
        else:
            st.sidebar.error("Welcome Back , Login Successsful")

# Main App Page - Blood Bank Finder
st.markdown(f"### Welcome to Karachi Blood Bank Finder 🩸")
st_lottie(lottie_animation, height=200)

# Blood Bank Finder Section
st.title("Find Blood Banks in Karachi")

# Data for Blood Banks with 20 Locations
blood_banks = pd.DataFrame([
    {"name": "Central Blood Bank", "location": "Saddar", "coordinates": (24.8607, 67.0011), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "City Blood Bank", "location": "Clifton", "coordinates": (24.8138, 67.0300), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Fatimid Foundation", "location": "North Nazimabad", "coordinates": (24.9425, 67.0728), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Indus Hospital", "location": "Korangi", "coordinates": (24.8205, 67.1279), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Liaquat National Hospital", "location": "Gulshan-e-Iqbal", "coordinates": (24.9215, 67.0954), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Aga Khan University Hospital", "location": "Karachi University", "coordinates": (24.8256, 67.0465), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "The Blood Bank", "location": "Ferozabad", "coordinates": (24.8880, 67.0708), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "JPMC Blood Bank", "location": "Saddar", "coordinates": (24.8556, 67.0092), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Karachi Blood Bank", "location": "Korangi", "coordinates": (24.8321, 67.0731), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Pakistan Red Crescent", "location": "Karachi City", "coordinates": (24.8772, 67.0240), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Sheikh Zayed Hospital", "location": "Abul Hasan Ispahani Road", "coordinates": (24.9402, 67.1212), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Quaid-e-Azam Blood Bank", "location": "Jamshed Road", "coordinates": (24.8700, 67.0142), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "National Blood Bank", "location": "Hassan Square", "coordinates": (24.8552, 67.0564), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Ziauddin Blood Bank", "location": "North Karachi", "coordinates": (24.9644, 67.0599), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Holy Family Blood Bank", "location": "Naya Nazimabad", "coordinates": (24.9271, 67.0505), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Tahir Blood Bank", "location": "Gulistan-e-Johar", "coordinates": (24.9286, 67.1201), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Pakistan Institute of Blood Transfusion", "location": "Saddar", "coordinates": (24.8522, 67.0202), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
    {"name": "Sindh Blood Transfusion Authority", "location": "Karachi", "coordinates": (24.9030, 67.0501), "blood_groups": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]},
])

# User Input for Blood Bank Finder (Always Visible)
with st.form("blood_bank_form"):
    location = st.selectbox("📍 Select Your Location", blood_banks["location"].unique())
    blood_group = st.selectbox("🩸 Select Required Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    submitted = st.form_submit_button("🔍 Find Blood Bank")

if submitted:
    st.markdown(f"### Blood Banks in **{location}** for **{blood_group}**")
    filtered_banks = blood_banks[blood_banks['location'] == location]
    available_banks = filtered_banks[filtered_banks['blood_groups'].apply(lambda x: blood_group in x)]
    
    if available_banks.empty:
        st.write("❌ No blood banks available with this blood group.")
    else:
        for index, bank in available_banks.iterrows():
            st.markdown(f"#### {bank['name']} - {bank['location']}")
            st.write(f"📍 Coordinates: {bank['coordinates']}")
            st.write("🩸 Blood Groups Available: " + ", ".join(bank['blood_groups']))
            st.write("---")

# Optional Log Out Button if Logged In
if "logged_in_user" in st.session_state:
    st.sidebar.button("Log Out", on_click=lambda: st.session_state.pop("logged_in_user"))
