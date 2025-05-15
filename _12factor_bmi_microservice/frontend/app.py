import streamlit as st
import requests
import json
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="🏋️",
    layout="centered"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .history-table {
        margin-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🏋️ BMI Calculator")
st.markdown("""
    Calculate your Body Mass Index (BMI) to check if you're at a healthy weight.
    Enter your details below to get started.
""")

# Input fields
with st.form("bmi_form"):
    name = st.text_input("Your Name")

    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, value=70.0, step=0.1)
    with col2:
        height = st.number_input("Height (m)", min_value=0.0, max_value=3.0, value=1.70, step=0.01)

    submit_button = st.form_submit_button("Calculate BMI")

# Handle form submission
if submit_button:
    if not name:
        st.error("Please enter your name")
    else:
        try:
            # Make API request
            response = requests.post(
                "http://localhost:8000/calculate-bmi",
                json={
                    "name": name,
                    "weight": weight,
                    "height": height
                }
            )

            if response.status_code == 200:
                result = response.json()

                # Display results in a nice format
                st.success(f"Hello {result['name']}, your BMI is: **{result['bmi']}**")
                st.info(f"Category: **{result['category']}**")

                # Add a visual indicator
                if result['category'] == "Normal weight":
                    st.balloons()

                # Add BMI scale visualization
                st.markdown("### BMI Scale")
                st.markdown("""
                    - Underweight: < 18.5
                    - Normal weight: 18.5 - 24.9
                    - Overweight: 25 - 29.9
                    - Obese: ≥ 30
                """)

            else:
                st.error("Error calculating BMI. Please check your inputs.")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the BMI calculation service. Please make sure the API is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# BMI History Section
st.markdown("---")
st.subheader("BMI History")

col1, col2 = st.columns([4, 1])
with col1:
    if st.button("Refresh History"):
        st.rerun()
with col2:
    if st.button("Clear History", type="secondary"):
        try:
            response = requests.delete("http://localhost:8000/bmi/history")
            if response.status_code == 200:
                st.success("History cleared successfully!")
                st.rerun()
        except Exception as e:
            st.error(f"Error clearing history: {str(e)}")

try:
    response = requests.get("http://localhost:8000/bmi/history")
    if response.status_code == 200:
        history = response.json()
        if history:
            # Convert the history data into a format suitable for display
            history_data = []
            for record in history:
                date = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
                history_data.append({
                    "Date": date.strftime("%Y-%m-%d %H:%M"),
                    "Name": record['name'],
                    "BMI": f"{record['bmi']:.2f}",
                    "Category": record['category'],
                    "Weight (kg)": f"{record['weight']:.1f}",
                    "Height (m)": f"{record['height']:.2f}"
                })
            st.table(history_data)
        else:
            st.info("No BMI records found. Calculate your first BMI!")
except requests.exceptions.ConnectionError:
    st.error("Could not connect to the BMI history service.")
except Exception as e:
    st.error(f"Error fetching BMI history: {str(e)}")

# Add helpful information
with st.expander("ℹ️ About BMI"):
    st.markdown("""
        BMI is a measure of body fat based on height and weight. While BMI is a useful screening tool,
        it's not diagnostic of body fatness or health. Factors such as age, sex, ethnicity, and muscle mass
        can influence the relationship between BMI and body fat.

        Always consult with healthcare professionals for a complete health assessment.
    """)