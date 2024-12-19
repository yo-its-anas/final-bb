import streamlit as st
import pandas as pd
import geopy.distance as geopy_distance
import requests
import random
import string
import time
import json

# Persistent User Storage (In-Memory for now)
users_db = {}

# Generate Random Username
def generate_username(name):
    return name.lower().replace(" ", "") + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

# Lottie animation for the header
def load_lottieurl(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

lottie_blood_bank = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_bx5dzv62.json")  # Lottie animation

# Set page configuration
st.set_page_config(page_title="Karachi Blood Bank Finder", layout="wide")

# Adding custom CSS for fonts, colors, and more elegant UI
st.markdown("""
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f7f7f7;
        }
        .card {
            background-color: #ffffff;
            padding: 20px;
            margin: 10px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .card h3 {
            color: #ff4c4c;
            font-size: 24px;
        }
        .card p {
            color: #333;
        }
        .header {
            text-align: center;
            color: #ff4c4c;
            font-size: 36px;
            margin-top: 20px;
        }
        .icon {
            color: #ff4c4c;
        }
        .button {
            background-color: #ff4c4c;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
        }
        .button:hover {
            background-color: #e00000;
        }
        .blood-bank-box {
            background-color: #fff0f0;
            border-radius: 10px;
            padding: 15px;
            margin: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        .blood-bank-header {
            color: #ff4c4c;
            font-size: 22px;
        }
        .blood-bank-content {
            color: #333;
            font-size: 16px;
        }
        .distance-text {
            color: #ff4c4c;
            font-size: 18px;
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
            st.sidebar.error("❌ Invalid Username or Password!")

# Main App Page - Blood Bank Finder
st.title("Find Blood Banks in Karachi")

st.json(lottie_blood_bank)  # Displaying the Lottie animation

# List of Areas in Karachi for the user to select
karachi_areas = [
    "Saddar", "Clifton", "Korangi", "Gulshan-e-Iqbal", "Malir", 
    "Numaish", "Jamshed Town", "Gulistan-e-Johar", "Shahrah-e-Faisal", 
    "Karachi Cantt", "Orangi Town", "Lyari", "Kharadar", "Korangi Creek", 
    "Bahria Town", "Lahore Colony", "Garden East", "Landhi"
]

# User Input for Location and Blood Group
user_location = st.selectbox("Select Your Location", karachi_areas)
selected_blood_group = st.selectbox("Select Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

# Data for Blood Banks
blood_banks = pd.DataFrame([
    {"name": "Central Blood Bank", "location": "Saddar", "coordinates": (24.8607, 67.0011), "blood_groups": ["A+", "O+"]},
    {"name": "City Blood Bank", "location": "Clifton", "coordinates": (24.8138, 67.0300), "blood_groups": ["B+", "AB+"]},
    {"name": "Fatimid Foundation", "location": "Numaish", "coordinates": (24.8726, 67.0437), "blood_groups": ["A-", "B-"]},
    {"name": "Hussaini Blood Bank", "location": "Malir", "coordinates": (24.8964, 67.1383), "blood_groups": ["O-", "AB+"]},
    {"name": "Indus Hospital Blood Bank", "location": "Korangi", "coordinates": (24.8497, 67.1398), "blood_groups": ["A+", "AB-"]},
    {"name": "Liaquat National Hospital Blood Bank", "location": "Gulshan-e-Iqbal", "coordinates": (24.9153, 67.0921), "blood_groups": ["O+", "B+"]},
    {"name": "Jinnah Hospital Blood Bank", "location": "Cantt", "coordinates": (24.8676, 67.0488), "blood_groups": ["A+", "B-"]},
])

if st.button("Find Blood Banks"):
    filtered_banks = blood_banks[blood_banks['blood_groups'].apply(lambda x: selected_blood_group in x) & (blood_banks['location'] == user_location)]
    if filtered_banks.empty:
        st.write("❌ No blood banks available for the selected blood group in your area.")
    else:
        for index, bank in filtered_banks.iterrows():
            distance = geopy_distance.distance((24.8607, 67.0011), bank['coordinates']).km
            st.markdown(
                f"""
                <div style="border: 2px solid #ff4c4c; border-radius: 10px; padding: 15px;">
                    <h3 style="color: #ff4c4c;">{bank['name']} - {bank['location']}</h3>
                    <p>🩸 Available Groups: {', '.join(bank['blood_groups'])}</p>
                    <p><strong>Distance:</strong> {distance:.2f} km</p>
                </div>
                """,
                unsafe_allow_html=True
            )
