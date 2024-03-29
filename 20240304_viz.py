import altair as alt
import pandas as pd
import streamlit as st

# Streamlit app setup
st.title('Pediatric Blood Pressure Percentiles (0 - 13 years old)')

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
    'Blood Pressure Value': [systolic_bp, diastolic_bp],  # Include actual BP values here
    'Blood Pressure Status': ['Normal BP' if 50 <= x < 90 else ('Elevated BP' if 90 <= x < 95 else 'Hypertension') if x >= 50 else '' for x in [systolic_percentile, diastolic_percentile]]
})

# Tooltip
tooltip_content = [
    alt.Tooltip('Type:N', title='Blood Pressure Type'),
    alt.Tooltip('Blood Pressure Value:Q', title='Blood Pressure Value'),  # Correctly reference BP values
    alt.Tooltip('Percentile:Q', title='Percentile'),
    alt.Tooltip('Blood Pressure Status:N', title='Blood Pressure Status'),
]

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

# Adding a calculated field for color based on conditions
data['Color'] = data['Percentile'].apply(lambda x: 'red' if x >= 95 else ('darkgoldenrod' if x >= 90 else ('darkgreen' if x > 50 else 'darkblue')))

# Base chart for points with conditional coloring based on the new 'Color' field
points = alt.Chart(data).mark_point(
    filled=True,
    size=100
).encode(
    x=alt.X('Age:Q', title='Age (years)', axis=alt.Axis(values=list(range(14))), scale=alt.Scale(domain=(0, 13))),
    y=alt.Y('Percentile:Q', title='Percentile', scale=alt.Scale(domain=(0, 100))),
    color=alt.Color('Color:N', legend=alt.Legend(title='Percentile Color'), scale=None),  # Directly use the 'Color' field
    tooltip=tooltip_content  # Include 'Blood Pressure Value' in the tooltip
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

# Adding the table below the chart
st.markdown("""
### Recommended Actions Based on Blood Pressure Status

| Blood Pressure Status | Actions |
|-----------------------|---------|
| **Normal BP** | - No additional action is needed<br>- BP should be rechecked at the next routine well-child care visit |
| **Elevated BP** | - Lifestyle interventions (nutrition, sleep, physical activity) should be initiated<br>- BP should be rechecked by auscultatory measurement in 6 months<br>- If BP remains elevated at 6 months, check upper and lower extremity BP and repeat lifestyle measures<br>- If BP is still elevated after 12 months from initial measurement, order ambulatory blood pressure monitoring along with diagnostic evaluation, and consider subspecialty referral |
| **Hypertension** | - If asymptomatic, initiate lifestyle interventions<br>- BP should be rechecked by auscultatory measurement in 1-2 weeks<br>- If it remains classified as hypertension at 1-2 weeks, check upper and lower extremity BP, and recheck BP in 3 months by auscultation with consideration for nutrition/weight management referral<br>- If BP continues to be classified as hypertension after 3 visits, order ambulatory blood pressure monitoring along with diagnostic evaluation, and initiate treatment with consideration for subspecialty referral |
""", unsafe_allow_html=True)