import altair as alt
import pandas as pd
import streamlit as st

# Sample function to calculate percentile based on age and height
# This is a placeholder, you should replace it with your actual formula
def calculate_percentiles(age, height, systolic_bp, diastolic_bp):
    # Placeholder logic for percentile calculation
    systolic_percentile = (height / age) * systolic_bp
    diastolic_percentile = (height / age) * diastolic_bp
    return systolic_percentile, diastolic_percentile

# Streamlit app
st.title('Blood Pressure Percentiles')

# User inputs
age = st.number_input('Enter age (years):', min_value=0, value=10)
height = st.number_input('Enter height (cm):', min_value=0, value=140)
systolic_bp = st.number_input('Enter systolic blood pressure (mmHg):', min_value=0, value=100)
diastolic_bp = st.number_input('Enter diastolic blood pressure (mmHg):', min_value=0, value=70)

# Calculate percentiles
systolic_percentile, diastolic_percentile = calculate_percentiles(age, height, systolic_bp, diastolic_bp)

# Create a DataFrame with the calculated percentiles
data = pd.DataFrame({
    'Age': [age, age],  # X-axis
    'Blood Pressure': [systolic_percentile, diastolic_percentile],  # Y-axis
    'Type': ['Systolic', 'Diastolic']  # Color/legend
})

# Create the Altair chart
chart = alt.Chart(data).mark_point().encode(
    x=alt.X('Age:Q', title='Age (years)'),
    y=alt.Y('Blood Pressure:Q', title='Blood pressure (mmHg)'),
    color=alt.Color('Type:N', title='Type')
).properties(
    title='Blood Pressure Percentiles'
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)