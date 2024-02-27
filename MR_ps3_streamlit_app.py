import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Dummy function to calculate blood pressure percentiles based on height and age
def calculate_percentiles(height, age):
    # These calculations are placeholders and should be replaced with real clinical data or formulas
    p50 = 100 + (height - 100) / 2 + (age - 10)
    p90 = p50 + 10
    p95 = p50 + 15
    p95_plus_12 = p50 + 27
    return p50, p90, p95, p95_plus_12

# Streamlit app
st.title("Blood Pressure Percentile Visualizer")

# User inputs
systolic_bp = st.number_input("Enter systolic blood pressure (mmHg):", min_value=50, max_value=200, value=120)
diastolic_bp = st.number_input("Enter diastolic blood pressure (mmHg):", min_value=30, max_value=120, value=80)
height = st.number_input("Enter height (cm):", min_value=100, max_value=200, value=150)
age = st.number_input("Enter age (years):", min_value=1, max_value=100, value=10)

# Calculate blood pressure percentiles based on height and age
p50, p90, p95, p95_plus_12 = calculate_percentiles(height, age)

# Plot
fig, ax = plt.subplots()
ax.set_xlim(0, 18)
ax.set_ylim(50, 150)
ax.set_xlabel('Age (years)')
ax.set_ylabel('Blood pressure (mmHg)')

# Plot percentiles as horizontal lines
ax.hlines(y=p50, xmin=0, xmax=18, colors='black', linestyles='dashed', label='50th percentile')
ax.hlines(y=p90, xmin=0, xmax=18, colors='black', linestyles='dashed', label='90th percentile')
ax.hlines(y=p95, xmin=0, xmax=18, colors='black', linestyles='dashed', label='95th percentile')
ax.hlines(y=p95_plus_12, xmin=0, xmax=18, colors='black', linestyles='dashed', label='95th percentile + 12 mmHg')

# Plot user-entered blood pressures
ax.plot(age, systolic_bp, 'o', label='Systolic BP')
ax.plot(age, diastolic_bp, 'o', label='Diastolic BP')

# Show legend
ax.legend()

# Display the plot
st.pyplot(fig)