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

# Assuming you have separate percentile data for Systolic and Diastolic BP
systolic_data = pd.DataFrame({
    'Age': [age] * 14,  # Repeat the age for each percentile
    'Percentile': list(range(50, 101)),  # Assuming you have percentiles from 50 to 100
    'Type': ['Systolic BP'] * 51  # Label each row as 'Systolic BP'
})

diastolic_data = pd.DataFrame({
    'Age': [age] * 14,  # Repeat the age for each percentile
    'Percentile': list(range(50, 101)),  # Assuming you have percentiles from 50 to 100
    'Type': ['Diastolic BP'] * 51  # Label each row as 'Diastolic BP'
})

# Combine the systolic and diastolic data
data = pd.concat([systolic_data, diastolic_data], ignore_index=True)

# Base chart for points
points = alt.Chart(data).mark_point().encode(
    x=alt.X('Age:Q', title='Age (years)', axis=alt.Axis(values=list(range(14))), scale=alt.Scale(domain=(0, 13))),
    y=alt.Y('Percentile:Q', title='Percentile', scale=alt.Scale(domain=(0, 100))),
    color=alt.Color('Type:N', legend=alt.Legend(title=None), sort=['Systolic BP', 'Diastolic BP']),
    tooltip=['Type', 'Percentile']
)

# Define filled areas for percentile ranges
area_50_to_90 = alt.Chart(data.query('Percentile == 50')).mark_area(color='lightgreen', opacity=0.5).encode(
    y='Percentile:Q',
    y2=alt.value(90)  # The top of the area is the 90th percentile
)

area_90_to_95 = alt.Chart(data.query('Percentile == 90')).mark_area(color='lightyellow', opacity=0.5).encode(
    y='Percentile:Q',
    y2=alt.value(95)  # The top of the area is the 95th percentile
)

area_above_95 = alt.Chart(data.query('Percentile == 95')).mark_area(color='lightred', opacity=0.5).encode(
    y='Percentile:Q',
    y2=alt.value(100)  # The top of the area is the 100th percentile
)

# Combine all chart layers
chart = alt.layer(
    area_50_to_90, area_90_to_95, area_above_95, points
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