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

# Hypothetical calculation for systolic and diastolic BP percentiles
# NOTE: This is a simplified and hypothetical example
def calculate_percentile(age, height, bp, bp_type="systolic"):
    # Hypothetical reference values (mean) based on age and height for systolic and diastolic
    reference_systolic = 90 + (age * 2) + (height * 0.1)
    reference_diastolic = 60 + (age * 1.5) + (height * 0.05)
    
    # Calculate deviation from reference value
    if bp_type == "systolic":
        deviation = bp - reference_systolic
    else:
        deviation = bp - reference_diastolic
    
    # Simplified percentile calculation (not statistically accurate)
    percentile = 50 + (deviation * 2)  # Assuming every 1 mmHg deviation shifts percentile by 2%
    percentile = np.clip(percentile, 0, 100)  # Ensure percentile is between 0 and 100
    return percentile

# Calculate percentiles
systolic_percentile = calculate_percentile(age, height, systolic_bp, "systolic")
diastolic_percentile = calculate_percentile(age, height, diastolic_bp, "diastolic")

# Display calculated percentiles
st.write(f"Systolic Blood Pressure Percentile: {systolic_percentile:.2f}%")
st.write(f"Diastolic Blood Pressure Percentile: {diastolic_percentile:.2f}%")

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

percentile_lines = alt.Chart(percentiles_df).mark_rule(color='black', size=1.5).encode(  # Set size to control line thickness
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

# Base chart for points
points = alt.Chart(data).mark_point().encode(
    x=alt.X('Age:Q', title='Age (years)', axis=alt.Axis(values=list(range(14))), scale=alt.Scale(domain=(0, 13))),
    y=alt.Y('Percentile:Q', title='Percentile', scale=alt.Scale(domain=(0, 100))),
    color=alt.Color('Type:N', legend=alt.Legend(title=None), sort=['Systolic BP', 'Diastolic BP']),  # Set legend title to None
    tooltip=['Type', 'Percentile']
)

# Combine all chart layers
chart = alt.layer(
    points, 
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