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

# Base chart for points
points = alt.Chart(data).mark_point().encode(
    x=alt.X('Age:Q', title='Age (years)', scale=alt.Scale(domain=(0, 13))),
    y=alt.Y('Percentile:Q', title='Percentile', scale=alt.Scale(domain=(0, 100))),
    color=alt.Color('Type:N', legend=alt.Legend(title=''), sort=['Systolic BP', 'Diastolic BP']),
    tooltip=['Type', 'Percentile']
)

# Function to create horizontal line and text for a given percentile
def percentile_line_and_text(percentile, color='black'):
    hline = alt.Chart(pd.DataFrame({'Percentile': [percentile]})).mark_rule(color=color).encode(
        y='Percentile:Q'
    )
    text = alt.Chart({'values':[{}]}).mark_text(
        align='left',
        baseline='middle',
        dx=7,  # Adjust x-position of the text
        text=f'{percentile}th Percentile',
        fontSize=12,
        color=color
    ).encode(
        y=alt.value(percentile)  # Y-position of the text
    )
    return hline, text

# Creating lines and texts for 50th, 90th, and 95th percentiles
hline_50, text_50 = percentile_line_and_text(50)
hline_90, text_90 = percentile_line_and_text(90)
hline_95, text_95 = percentile_line_and_text(95)

# Layering the charts
chart = alt.layer(
    points, 
    hline_50, text_50,
    hline_90, text_90,
    hline_95, text_95
).properties(
    title='Blood Pressure Percentiles by Age',
    width='container',
    height=300
).configure_view(
    strokeWidth=0
).configure_axis(
    labelPadding=10,
    titlePadding=10
).configure_axis(grid=False)  # Disable grid lines

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)