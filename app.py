import streamlit as st
import json
from streamlit_lottie import st_lottie
import random

# Helper Function to Load Lottie Animation
def load_lottie_animation(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Dummy Data for Blood Banks and Areas
blood_banks = [
    {"name": "City Blood Bank", "area": "Saddar", "contact": "0300-1234567", "website": "www.citybloodbank.com", "distance": "2 km"},
    {"name": "Jinnah Blood Bank", "area": "Gulshan-e-Iqbal", "contact": "0301-7654321", "website": "www.jinnahbloodbank.com", "distance": "5 km"},
    # Add 18 more dummy entries here...
]

areas = ["Saddar", "Gulshan-e-Iqbal", "Defence", "Clifton", "Nazimabad", "North Karachi", "Korangi", "Liaquatabad", 
         "Malir", "Orangi Town", "Gulistan-e-Johar", "PECHS", "Shah Faisal Colony", "FB Area", "Garden", "Bahadurabad", 
         "Tariq Road", "Landhi", "Kemari", "SITE Area"]

# UI Configuration
st.set_page_config(page_title="Karachi Blood Bank Finder", page_icon="🩸", layout="wide")

# Load Lottie Animation
animation = load_lottie_animation("assets/animation.json")

# App Header
st.title("🩸 Karachi Blood Bank Finder")
st.markdown("Find the nearest blood bank in Karachi based on your location and required blood group.")

# Show Lottie Animation
st_lottie(animation, height=300, key="animation")

# Login or Sign-Up Option
st.sidebar.title("Dashboard")
choice = st.sidebar.selectbox("Login/Signup", ["Login", "Signup", "Home"])

if choice == "Signup":
    st.sidebar.subheader("Create an Account")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    email = st.sidebar.text_input("Email")
    phone = st.sidebar.text_input("Phone")
    if st.sidebar.button("Sign Up"):
        st.sidebar.success("Account Created! Please Login.")
elif choice == "Login":
    st.sidebar.subheader("Login to Your Account")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        st.sidebar.success("Logged in Successfully!")
else:
    # Main App Logic
    st.header("Find a Blood Bank")
    user_location = st.selectbox("Select Your Area", areas)
    blood_group = st.selectbox("Select Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

    if st.button("Find Blood Bank"):
        results = [
            bank for bank in blood_banks
            if bank["area"] == user_location
        ]

        if results:
            for bank in results:
                st.markdown(
                    f"""
                    <div style="border: 1px solid #ccc; padding: 15px; border-radius: 10px; margin-bottom: 15px; background-color: #f9f9f9;">
                        <h3>{bank['name']}</h3>
                        <p><strong>Area:</strong> {bank['area']}</p>
                        <p><strong>Contact:</strong> {bank['contact']}</p>
                        <p><strong>Website:</strong> <a href="https://{bank['website']}" target="_blank">{bank['website']}</a></p>
                        <p><strong>Distance:</strong> {bank['distance']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("No blood banks found in your area.")

st.sidebar.info("This app is for demonstration purposes only.")
