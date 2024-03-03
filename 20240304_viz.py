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
    'Age': [age for i in range(100)],  # Generate data across the percentile range
    'Percentile': list(range(1, 101)),  # 1st to 100th percentile
    'Type': ['Systolic BP' if i < 50 else 'Diastolic BP' for i in range(100)]
})

# NHANES data placeholder function
@st.cache
def load_csv(file_path):
    return pd.read_csv(file_path)
# data = load_csv('nhanes/nhanes_clean.csv')

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
    x=alt.value(344.5),  # You may need to adjust this value
    y='Percentile:Q',
    text='Label:N'
)

# Base chart for points
points = alt.Chart(data).mark_point(
    filled=True,
    size=100
).encode(
    x=alt.X('Age:Q', title='Age (years)'),
    y=alt.Y('Percentile:Q', title='Percentile'),
    color=alt.Color('Type:N', legend=alt.Legend(title=None)),
    tooltip=['Type', 'Percentile']
)

# Creating an area chart to fill above the 50th percentile
filled_area = alt.Chart(data).mark_area(
    color="lightgreen",
    opacity=0.5
).encode(
    x='Age:Q',
    y='Percentile:Q'
).transform_filter(
    alt.datum.Percentile > 50  # This ensures we only fill above the 50th percentile
)

# Combine all chart layers
chart = alt.layer(
    filled_area, points, percentile_lines, percentile_labels
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
