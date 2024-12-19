import streamlit as st
import pandas as pd
import geopy.distance as geopy_distance
import requests
import random
import string

# Function to load Lottie animation (cached for faster load)
@st.cache_data
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
        .stylish-box {
            background-color: #ffffff;
            padding: 15px;
            margin: 10px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #1e90ff;
        }
        .blue-link {
            color: #1e90ff;
            text-decoration: underline;
        }
        .header, .stylish-box h3 {
            color: #1e90ff;
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
        if username_input and password_input:
            st.session_state["logged_in_user"] = username_input
            st.sidebar.success(f"👋 Welcome, {username_input}!")
            st.markdown(f"## Hello {username_input}, welcome to the Karachi Blood Bank Finder! 😊")
            st.sidebar.button("Log Out", on_click=lambda: st.session_state.pop("logged_in_user"))
        else:
            st.sidebar.error("❌ Please enter a valid Username and Password.")

# Main App Page - Blood Bank Finder
st.markdown(f"### Welcome to Karachi Blood Bank Finder 🩸")
st.json(lottie_animation)  # This will load the old animation

# Blood Bank Finder Section
st.title("Find Blood Banks in Karachi")

# Data for Blood Banks with 20 Locations (Reduced set for performance)
blood_banks = pd.DataFrame([
    {"name": "Central Blood Bank", "location": "Saddar", "coordinates": (24.8607, 67.0011), "blood_groups": ["A+", "O+"]},
    {"name": "City Blood Bank", "location": "Clifton", "coordinates": (24.8138, 67.0300), "blood_groups": ["B+", "AB+"]},
    {"name": "Fatimid Foundation", "location": "North Nazimabad", "coordinates": (24.9425, 67.0728), "blood_groups": ["A-", "O+"]},
    {"name": "Indus Hospital", "location": "Korangi", "coordinates": (24.8205, 67.1279), "blood_groups": ["O-", "B+"]},
    {"name": "Liaquat National Hospital", "location": "Gulshan-e-Iqbal", "coordinates": (24.9215, 67.0954), "blood_groups": ["A+", "AB-"]},
])

# User Input for Blood Bank Finder (Always Visible)
with st.form("blood_search"):
    blood_group_needed = st.selectbox("Select Required Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    user_location = st.text_input("Enter your Location (City Name)")

    submit_button = st.form_submit_button("Search Blood Banks")

# Display available blood banks
if submit_button:
    if user_location.strip():
        st.subheader("Available Blood Banks near you:")
        available_banks = blood_banks[blood_banks["blood_groups"].apply(lambda x: blood_group_needed in x)]
        if available_banks.empty:
            st.markdown(f"🔍 Searching for nearest blood banks with **{blood_group_needed}**...")
            
            # Pre-calculated sample location (Karachi)
            user_coordinates = (24.8607, 67.0011)
            
            # Calculate nearest available blood banks
            available_banks = blood_banks.copy()
            available_banks['distance'] = available_banks['coordinates'].apply(lambda x: geopy_distance.distance(user_coordinates, x).km)
            nearest_banks = available_banks.sort_values("distance").head(3)
            
            for _, bank in nearest_banks.iterrows():
                st.markdown(f"### {bank['name']}")
                st.markdown(f"📍 Location: {bank['location']}")
                st.markdown(f"🩸 Available Blood Groups: {', '.join(bank['blood_groups'])}")
                st.markdown(f"📞 Contact: +92-{random.randint(3000000000, 3999999999)}")
                st.markdown(f"🌐 Website: [Visit]({bank['name'].lower().replace(' ', '')}.domain.com)")
                st.markdown(f"📍 Distance: {round(bank['distance'], 2)} km")
                st.markdown("---")
        else:
            for _, bank in available_banks.iterrows():
                st.markdown(f"""
                    <div class="stylish-box">
                        <h3>{bank['name']}</h3>
                        <p>📍 Location: {bank['location']}</p>
                        <p>🩸 Available Blood Groups: {', '.join(bank['blood_groups'])}</p>
                        <p>📞 Contact: +92-{random.randint(3000000000, 3999999999)}</p>
                        <p>🌐 Website: <a href="http://{bank['name'].lower().replace(' ', '')}.domain.com" class="blue-link" target="_blank">Visit</a></p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Please enter a location.")
