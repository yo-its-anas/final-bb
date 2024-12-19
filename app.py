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

# Set page configuration
st.set_page_config(page_title="Karachi Blood Bank Finder", layout="wide")

st.sidebar.title("🔒 User Authentication")
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
            st.sidebar.success(f"🎉 Account created successfully for **{name}**")
        else:
            st.sidebar.error("❌ Please fill in all fields!")

elif auth_option == "Sign In":
    st.sidebar.header("Log In")
    with st.sidebar.form("signin_form"):
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        signin_submit = st.form_submit_button("Sign In")

    if signin_submit:
        if username_input and password_input:
            st.sidebar.success(f"👋 Welcome, {username_input}!")
        else:
            st.sidebar.error("❌ Invalid credentials!")

# Blood Bank Finder Section
st.title("Find Blood Banks in Karachi")

# Blood Bank Data
blood_banks = pd.DataFrame([
    {"name": "Central Blood Bank", "location": "Saddar", "coordinates": (24.8607, 67.0011), "blood_groups": ["A+","B+", "O+"]},
    {"name": "City Blood Bank", "location": "Clifton", "coordinates": (24.8138, 67.0300), "blood_groups": ["B+","O-". "AB+"]},
    {"name": "Fatimid Foundation", "location": "North Nazimabad", "coordinates": (24.9425, 67.0728), "blood_groups": ["A-", "O+","O-"]},
    {"name": "Indus Hospital", "location": "Korangi", "coordinates": (24.8205, 67.1279), "blood_groups": ["O-", "B+"]},
    {"name": "Liaquat National Hospital", "location": "Gulshan-e-Iqbal", "coordinates": (24.9215, 67.0954), "blood_groups": ["A+", "AB-"]},
    {"name": "Aga Khan University Hospital", "location": "Karachi University", "coordinates": (24.8256, 67.0465), "blood_groups": ["O-", "AB+"]},
    {"name": "The Blood Bank", "location": "Ferozabad", "coordinates": (24.8880, 67.0708), "blood_groups": ["A-", "B-"]},
    {"name": "JPMC Blood Bank", "location": "Saddar", "coordinates": (24.8556, 67.0092), "blood_groups": ["B+", "O+"]},
    {"name": "Karachi Blood Bank", "location": "Korangi", "coordinates": (24.8321, 67.0731), "blood_groups": ["O-","B+", "A+"]},
    {"name": "Pakistan Red Crescent", "location": "Karachi City", "coordinates": (24.8772, 67.0240), "blood_groups": ["AB-", "O+"]},
    {"name": "Sheikh Zayed Hospital", "location": "Abul Hasan Ispahani Road", "coordinates": (24.9402, 67.1212), "blood_groups": ["A-", "AB+"]},
    {"name": "Quaid-e-Azam Blood Bank", "location": "Jamshed Road", "coordinates": (24.8700, 67.0142), "blood_groups": ["A+","O-", "B+"]},
    {"name": "National Blood Bank", "location": "Hassan Square", "coordinates": (24.8552, 67.0564), "blood_groups": ["O-", "A+"]},
    {"name": "Ziauddin Blood Bank", "location": "North Karachi", "coordinates": (24.9644, 67.0599), "blood_groups": ["AB+", "B+"]},
    {"name": "Holy Family Blood Bank", "location": "Naya Nazimabad", "coordinates": (24.9271, 67.0505), "blood_groups": ["O+", "AB-"]},
    {"name": "Tahir Blood Bank", "location": "Gulistan-e-Johar", "coordinates": (24.9286, 67.1201), "blood_groups": ["B-", "O+"]},
    {"name": "Pakistan Institute of Blood Transfusion", "location": "Saddar", "coordinates": (24.8522, 67.0202), "blood_groups": ["A-","O-", "B+"]},
    {"name": "Sindh Blood Transfusion Authority", "location": "Karachi", "coordinates": (24.9030, 67.0501), "blood_groups": ["AB-","O-", "O+"]},
])

with st.form("blood_search"):
    blood_group_needed = st.selectbox("Select Required Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    selected_location = st.selectbox("Select Your Location", blood_banks["location"].unique())
    submit_button = st.form_submit_button("Search Blood Banks")

if submit_button:
    available_banks = blood_banks[(blood_banks["blood_groups"].apply(lambda x: blood_group_needed in x)) & (blood_banks["location"] == selected_location)]
    if available_banks.empty:
        st.warning(f"❌ No blood banks with **{blood_group_needed}** in **{selected_location}**.")
    else:
        for _, bank in available_banks.iterrows():
            st.markdown(f"### {bank['name']} - {bank['location']}")
            st.markdown(f"🩸 Available Blood Groups: {', '.join(bank['blood_groups'])}")
