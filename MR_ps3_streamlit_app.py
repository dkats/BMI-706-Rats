import altair as alt
import pandas as pd
import streamlit as st

# Streamlit app
st.title('Blood Pressure Percentiles')

# User inputs
sex = st.radio('Select sex:', ('Male', 'Female'))
age = st.slider('Select age (years):', min_value=0, max_value=13, value=10)
height = st.number_input('Enter height (inches):', min_value=0, value=50)
systolic_bp = st.number_input('Enter systolic blood pressure (mmHg):', min_value=0, value=96)
diastolic_bp = st.number_input('Enter diastolic blood pressure (mmHg):', min_value=0, value=60)

# Assuming that there is a function to calculate the percentile
# For now, we are just taking the provided percentiles as they are
# In a real scenario, you would calculate the percentiles based on the inputs
systolic_percentile = systolic_bp - 50   # Placeholder, replace with your calculation
diastolic_percentile = diastolic_bp - 50 # Placeholder, replace with your calculation

# Create a DataFrame with the calculated percentiles
data = pd.DataFrame({
    'Age': [age, age],  # X-axis
    'Percentile': [systolic_percentile, diastolic_percentile],  # Y-axis
    'Type': ['Systolic BP', 'Diastolic BP']  # Color/legend
})

# Create the Altair chart
chart = alt.Chart(data).mark_point().encode(
    x=alt.X('Age:Q', title='Age (years)', scale=alt.Scale(domain=(0, 13))),
    y=alt.Y('Percentile:Q', title='Blood Pressure Percentile', scale=alt.Scale(domain=(0, 100))),
    color=alt.Color('Type:N', title='Blood Pressure Type'),
    tooltip=['Type', 'Percentile']
).properties(
    title='Blood Pressure Percentiles by Age'
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)