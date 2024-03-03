import altair as alt
import pandas as pd
import streamlit as st

# Streamlit app setup
st.title('Pediatric Blood Pressure Percentiles')

# User inputs
sex = st.radio('Select sex:', ('Male', 'Female'))
age = st.slider('Select age (years):', min_value=0, max_value=13, value=10)
height = st.number_input('Enter height (cm):', min_value=0, value=50)
systolic_bp = st.number_input('Enter systolic blood pressure (mmHg):')
diastolic_bp = st.number_input('Enter diastolic blood pressure (mmHg):')

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

# Corrected function to determine the symbol based on percentile
def get_symbol(percentile):
    if percentile >= 95:
        return '‼'  # Two exclamation points for equal to or greater than 95th percentile
    elif percentile >= 90:
        return '!'   # One exclamation point for equal to or greater than 90th percentile
    elif percentile > 50:
        return '✔'  # Check mark for above 50th percentile
    else:
        return ''    # No symbol for 50th percentile or below

# Apply the corrected symbol logic to the DataFrame
data['Symbol'] = data['Percentile'].apply(get_symbol)

# Updated tooltip contents to include blood pressure values
tooltip_content = [
    alt.Tooltip('Type:N', title='Blood Pressure Type'),
    alt.Tooltip('Blood Pressure Value:Q', title='Blood Pressure Value'),  # Correctly reference BP values
    alt.Tooltip('Percentile:Q', title='Percentile')
]

# Base chart for symbols with the corrected x-axis range and increments
symbols = alt.Chart(data).mark_text(
    size=20,  # Adjust text size as needed
    fontSize=15,  # Adjust font size for better visibility and fitting within circles
    color='black'  # Set the symbol color to black
).encode(
    x=alt.X('Age:Q', title='Age (years)', scale=alt.Scale(domain=(0, 13)), axis=alt.Axis(tickCount=13)),
    y=alt.Y('Percentile:Q', title='Percentile'),
    text='Symbol:N',
    tooltip=tooltip_content
)

# Chart for circular outlines
circles = alt.Chart(data).mark_circle(
    size=300,  # Adjust circle size as needed
    color='none',  # No fill color for the circles
    stroke='black'  # Outline color
).encode(
    x=alt.X('Age:Q'),
    y=alt.Y('Percentile:Q')
)

# Combine symbols and circles using alt.layer()
combined = alt.layer(circles, symbols)

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
    combined,  # Circles and symbols combined
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
