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

# Placeholder values for the percentiles
systolic_percentile = 51  # Example value
diastolic_percentile = 56  # Example value

# Ensure the order in the DataFrame matches the desired legend order
data = pd.DataFrame({
    'Age': [age, age],
    'Percentile': [systolic_percentile, diastolic_percentile],
    'Type': ['Systolic BP', 'Diastolic BP']
})

# Create the Altair chart with explicit sorting for the legend
chart = alt.Chart(data).mark_point().encode(
    x=alt.X('Age:Q', title='Age (years)', scale=alt.Scale(domain=(0, 13))),
    y=alt.Y('Percentile:Q', title='Percentile', scale=alt.Scale(domain=(0, 100))),
    color=alt.Color('Type:N', legend=alt.Legend(title=''), sort=['Systolic BP', 'Diastolic BP']),
    tooltip=['Type', 'Percentile']
).properties(
    title='Blood Pressure Percentiles by Age'
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)