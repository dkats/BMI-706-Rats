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
    'Type': ['Systolic BP', 'Diastolic BP'],
    'Blood Pressure Value': [systolic_bp, diastolic_bp]  # Include actual BP values here
})

# Define a color scale for the percentiles
def get_color(percentile):
    if percentile >= 95:
        return 'red'
    elif percentile >= 90:
        return 'orange'
    elif percentile > 50:
        return 'green'
    else:
        return 'lightgrey'

# Apply the color scale to the DataFrame
data['Color'] = data['Percentile'].apply(get_color)

# Chart for colored circles
colored_circles = alt.Chart(data).mark_circle(
    size=300,  # Adjust circle size as needed
).encode(
    x=alt.X('Age:Q', title='Age (years)', scale=alt.Scale(domain=(0, 13)), axis=alt.Axis(tickCount=13)),
    y=alt.Y('Percentile:Q', title='Percentile'),
    color=alt.Color('Color:N', legend=None),  # Use the color encoding
    tooltip=[
        alt.Tooltip('Type:N', title='Blood Pressure Type'),
        alt.Tooltip('Blood Pressure Value:Q', title='Blood Pressure Value'),  # Include BP value in tooltip
        alt.Tooltip('Percentile:Q', title='Percentile')
    ]
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
    y='Percentile:Q',
    text='Label:N'
)

# Combine all chart layers
chart = alt.layer(
    colored_circles,
    percentile_lines,
    percentile_labels
).properties(
    title='',
    width='container',
    height=350
).configure_view(
    strokeWidth=0
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)
