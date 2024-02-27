import altair as alt
import pandas as pd
import streamlit as st

# Streamlit app setup
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

# Data for the chart
data = pd.DataFrame({
    'Age': [age, age],
    'Percentile': [systolic_percentile, diastolic_percentile],
    'Type': ['Systolic BP', 'Diastolic BP']
})

# Define horizontal lines for the 50th, 90th, and 95th percentiles
percentiles_df = pd.DataFrame({
    'Percentile': [50, 90, 95],
    'Label': ['50th', '90th', '95th']
})

percentile_lines = alt.Chart(percentiles_df).mark_rule(color='black').encode(
    y='Percentile:Q'
)

# Add labels for each percentile line
percentile_labels = percentile_lines.mark_text(
    align='left',
    dx=.1,  # Distance from the right edge
    dy=-5,  # Distance above the line
    text='Label:N'
).encode(
    x=alt.value(350),  # Adjust this value based on the plot width or container width
    y='Percentile:Q',
    text='Label:N'
)

# Base chart for points
points = alt.Chart(data).mark_point().encode(
    x=alt.X('Age:Q', title='Age (years)', scale=alt.Scale(domain=(0, 13))),
    y=alt.Y('Percentile:Q', title='Percentile', scale=alt.Scale(domain=(0, 100))),
    color=alt.Color('Type:N', legend=alt.Legend(title=''), sort=['Systolic BP', 'Diastolic BP']),
    tooltip=['Type', 'Percentile']
)

# Combine all chart layers
chart = alt.layer(
    points, 
    percentile_lines, 
    percentile_labels
).properties(
    title='Blood Pressure Percentiles by Age',
    width='container',
    height=300
).configure_view(
    strokeWidth=0
).configure_axis(
    labelPadding=10,
    titlePadding=10,
    grid=False
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)