import streamlit as st
import pandas as pd
import geopy.distance as geopy_distance
import requests
import random
import string
import time
from streamlit_lottie import st_lottie  # Importing Lottie

def load_lottie_url(url):
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raise an error for any HTTP issues
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Lottie animation: {e}")
        return None
    except ValueError:
        st.error("Invalid JSON returned from Lottie URL.")
        return None

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
# The code before this line remains unchanged...

# Main App Page - Blood Bank Finder
st.markdown(f"### Welcome to Karachi Blood Bank Finder 🩸")

# Removed automatic Lottie animation as per new UI guidelines
lottie_loading_ring = load_lottie_url("https://assets9.lottiefiles.com/private_files/lf30_editor_nueh7zpx.json")

st.title("Find Blood Banks in Karachi")

# User Input for Location and Blood Group
user_location = st.selectbox("Select Your Location", blood_banks['location'].unique())
selected_blood_group = st.selectbox("Select Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

# Button to start finding blood banks
if st.button("Find Blood Banks"):
    with st.spinner("⏳ Finding blood banks..."):
        time.sleep(5)  # 5-second delay to simulate loading
    # Display Blood Banks Matching the Criteria
    st.markdown("#### Available Blood Banks:")
    
    filtered_banks = blood_banks[blood_banks['blood_groups'].apply(lambda x: selected_blood_group in x)]
    
    if filtered_banks.empty:
        st.write("❌ No blood banks available for the selected blood group.")
    else:
        for index, bank in filtered_banks.iterrows():
            # Calculate distance from user's location (for simplicity, assume the user is in the center)
            user_coords = (24.8607, 67.0011)  # Karachi's approximate center coordinates
            bank_coords = bank['coordinates']
            distance = geopy_distance.distance(user_coords, bank_coords).km
            
            # Blood Bank Card with border for clarity
            st.markdown(
                f"""
                <div style="border: 2px solid #ff4c4c; border-radius: 10px; padding: 15px; margin: 15px;">
                    <h3 style="color: #ff4c4c;">{bank['name']} - {bank['location']}</h3>
                    <p>📍 Coordinates: {bank['coordinates']}</p>
                    <p>🩸 Blood Groups Available: {', '.join(bank['blood_groups'])}</p>
                    <p><strong>Distance:</strong> {distance:.2f} km</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# The rest of your code continues unchanged...




# Data for Blood Banks with 20 Locations
blood_banks = pd.DataFrame([
    {"name": "Central Blood Bank", "location": "Saddar", "coordinates": (24.8607, 67.0011), "blood_groups": ["A+", "O+"]},
    {"name": "City Blood Bank", "location": "Clifton", "coordinates": (24.8138, 67.0300), "blood_groups": ["B+", "AB+"]},
    {"name": "Fatimid Foundation", "location": "North Nazimabad", "coordinates": (24.9425, 67.0728), "blood_groups": ["A-", "O+"]},
    {"name": "Indus Hospital", "location": "Korangi", "coordinates": (24.8205, 67.1279), "blood_groups": ["O-", "B+"]},
    {"name": "Liaquat National Hospital", "location": "Gulshan-e-Iqbal", "coordinates": (24.9215, 67.0954), "blood_groups": ["A+", "AB-"]},
    {"name": "Aga Khan University Hospital", "location": "Karachi University", "coordinates": (24.8256, 67.0465), "blood_groups": ["O-", "AB+"]},
    {"name": "The Blood Bank", "location": "Ferozabad", "coordinates": (24.8880, 67.0708), "blood_groups": ["A-", "B-"]},
    {"name": "JPMC Blood Bank", "location": "Saddar", "coordinates": (24.8556, 67.0092), "blood_groups": ["B+", "O+"]},
    {"name": "Karachi Blood Bank", "location": "Korangi", "coordinates": (24.8321, 67.0731), "blood_groups": ["O-", "A+"]},
    {"name": "Pakistan Red Crescent", "location": "Karachi City", "coordinates": (24.8772, 67.0240), "blood_groups": ["AB-", "O+"]},
    {"name": "Sheikh Zayed Hospital", "location": "Abul Hasan Ispahani Road", "coordinates": (24.9402, 67.1212), "blood_groups": ["A-", "AB+"]},
    {"name": "Quaid-e-Azam Blood Bank", "location": "Jamshed Road", "coordinates": (24.8700, 67.0142), "blood_groups": ["A+", "B+"]},
    {"name": "National Blood Bank", "location": "Hassan Square", "coordinates": (24.8552, 67.0564), "blood_groups": ["O-", "A+"]},
    {"name": "Ziauddin Blood Bank", "location": "North Karachi", "coordinates": (24.9644, 67.0599), "blood_groups": ["AB+", "B+"]},
    {"name": "Holy Family Blood Bank", "location": "Naya Nazimabad", "coordinates": (24.9271, 67.0505), "blood_groups": ["O+", "AB-"]},
    {"name": "Tahir Blood Bank", "location": "Gulistan-e-Johar", "coordinates": (24.9286, 67.1201), "blood_groups": ["B-", "O+"]},
    {"name": "Pakistan Institute of Blood Transfusion", "location": "Saddar", "coordinates": (24.8522, 67.0202), "blood_groups": ["A-", "B+"]},
    {"name": "Sindh Blood Transfusion Authority", "location": "Karachi", "coordinates": (24.9030, 67.0542), "blood_groups": ["A+", "B+"]},
    {"name": "Zainab Blood Bank", "location": "Korangi", "coordinates": (24.8231, 67.1189), "blood_groups": ["O-", "A+"]},
    {"name": "Dawood Blood Bank", "location": "Clifton", "coordinates": (24.8052, 67.0321), "blood_groups": ["AB-", "B+"]},
])

# User Input for Location and Blood Group
user_location = st.selectbox("Select Your Location", blood_banks['location'].unique())
selected_blood_group = st.selectbox("Select Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

# Simulate delay before showing results
with st.spinner("⏳ Finding blood banks..."):
    time.sleep(5)  # 5-second delay to simulate loading

# Display Blood Banks Matching the Criteria
st.markdown("#### Available Blood Banks:")

filtered_banks = blood_banks[blood_banks['blood_groups'].apply(lambda x: selected_blood_group in x)]

if filtered_banks.empty:
    st.write("❌ No blood banks available for the selected blood group.")
else:
    for index, bank in filtered_banks.iterrows():
        # Calculate distance from user's location (for simplicity, assume the user is in the center)
        user_coords = (24.8607, 67.0011)  # Karachi's approximate center coordinates
        bank_coords = bank['coordinates']
        distance = geopy_distance.distance(user_coords, bank_coords).km
        
        # Blood Bank Card
        with st.expander(f"{bank['name']} - {bank['location']}"):
            st.markdown(f"#### {bank['name']}")
            st.write(f"📍 Coordinates: {bank['coordinates']}")
            st.write(f"🩸 Blood Group Available: {', '.join(bank['blood_groups'])}")
            st.markdown(f"**Distance**: {distance:.2f} km")
            st.write("---")

# Optional Log Out Button if Logged In
if "logged_in_user" in st.session_state:
    st.sidebar.button("Log Out", on_click=lambda: st.session_state.pop("logged_in_user"))
