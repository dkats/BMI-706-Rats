import altair as alt
import pandas as pd
import streamlit as st
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects

# Ensure that rpy2's pandas2ri is activated to automatically convert r objects to pandas dataframes
pandas2ri.activate()

# Import the R package (replace 'pedbp' with the actual name of your package)
pedbp = importr('pedbp')

# Streamlit app setup
st.title('Pediatric Blood Pressure Percentiles')

# User inputs
sex = st.radio('Select sex:', ('Male', 'Female'))
age_years = st.slider('Select age (years):', min_value=0, max_value=13, value=10)
height = st.number_input('Enter height (cm):', min_value=0, value=50)
systolic_bp = st.number_input('Enter systolic blood pressure (mmHg):', min_value=0, value=96)
diastolic_bp = st.number_input('Enter diastolic blood pressure (mmHg):', min_value=0, value=60)

# Convert age from years to months for the R function
age_months = age_years * 12

# Convert sex from string to binary indicator for male
male = 1 if sex == 'Male' else 0

# Prepare the call to the R function
r_function = robjects.r['p_bp']
result = r_function(q_sbp=systolic_bp, q_dbp=diastolic_bp, age=age_months, male=male, height=height)

# Extracting percentiles from the result
sbp_percentile = result.rx('sbp_percentile')[0][0] * 100  # Multiply by 100 to convert to percentage
dbp_percentile = result.rx('dbp_percentile')[0][0] * 100  # Multiply by 100 to convert to percentage

# Display the calculated percentiles
st.write(f"Systolic BP Percentile: {sbp_percentile:.2f}%")
st.write(f"Diastolic BP Percentile: {dbp_percentile:.2f}%")

# Prepare data for the chart
data = pd.DataFrame({
    'Age': [age_years for _ in range(2)],  # Use age_years for display purposes
    'Percentile': [sbp_percentile, dbp_percentile],
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