import altair as alt
import pandas as pd
import streamlit as st

# Streamlit app setup
st.title('Pediatric Blood Pressure Percentiles')

# User inputs
sex = st.radio('Select sex:', ('Male', 'Female'))
age = st.slider('Select age (years):', min_value=0, max_value=13, value=10)
height = st.number_input('Enter height (cm):', min_value=0, value=50)
systolic_bp = st.number_input('Enter systolic blood pressure (mmHg):', min_value=0, value=96)
diastolic_bp = st.number_input('Enter diastolic blood pressure (mmHg):', min_value=0, value=60)

# Placeholder values for the percentiles
systolic_percentile = systolic_bp + age - height  # Example value
diastolic_percentile = diastolic_bp + age - height # Example value

# Data for the chart
data = pd.DataFrame({
    'Age': [age, age],
    'Percentile': [systolic_percentile, diastolic_percentile],
    'Type': ['Systolic BP', 'Diastolic BP']
})

# Function to determine the symbol
data['Symbol'] = data['Percentile'].apply(lambda x: '‼' if x >= 95 else ('!' if x >= 90 else ('✔' if x > 50 else '.')))

# Chart for symbols
symbols = alt.Chart(data).mark_text(
    size=20,  # Adjust text size as needed
).encode(
    x=alt.X('Age:Q', title='Age (years)'),
    y=alt.Y('Percentile:Q', title='Percentile'),
    text='Symbol:N',
    tooltip=['Type', 'Percentile']
)

# Chart for circular outlines
circles = alt.Chart(data).mark_circle(
    size=150,  # Adjust circle size as needed
    color='none',  # No fill color for the circles
    stroke='black'  # Outline color
).encode(
    x=alt.X('Age:Q', title='Age (years)'),
    y=alt.Y('Percentile:Q', title='Percentile'),
)

# Define horizontal lines for the 50th, 90th, and 95th percentiles
percentiles_df = pd.DataFrame({
    'Percentile': [50, 90, 95],
    'Label': ['50th', '90th', '95th']
})

percentile_lines = alt.Chart(percentiles_df).mark_rule(color='black', size=1.5).encode(
    y='Percentile:Q'
)

# Add labels for each percentile line
percentile_labels = percentile_lines.mark_text(
    align='right',
    dx=-2,
    dy=-5,
    text='Label:N'
).encode(
    x=alt.value(344.5),
    y='Percentile:Q',
    text='Label:N'
)

# Combine all chart layers
chart = alt.layer(
    circles,  # Circular outlines
    symbols,  # Text symbols
    percentile_lines,
    percentile_labels
).properties(
    title='',
    width='container',
    height=350
).configure_view(
    strokeWidth=0
).configure_axis(
    labelPadding=5,
    titlePadding=5,
    grid=False
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)
