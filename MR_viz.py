import altair as alt
import pandas as pd
import scipy.stats as stats
import streamlit as st

# Function to calculate percentile
def calc_percentile(value, percentile_50, percentile_95):
    sigma = (percentile_95 - percentile_50) / 1.645
    return stats.norm.cdf((value - percentile_50) / sigma) * 100

# Load BP tables
pertable_fd = pd.read_csv('bp-tables/FemaleDBP.csv')
pertable_fs = pd.read_csv('bp-tables/FemaleSBP.csv')
pertable_md = pd.read_csv('bp-tables/MaleDBP.csv')
pertable_ms = pd.read_csv('bp-tables/MaleSBP.csv')

# Streamlit app setup
st.title('Pediatric Blood Pressure Percentiles for Screening and Management of High Blood Pressure (0-13 years old)')

# Load NHANES
nhanes = pd.read_csv('nhanes/nhanes_clean.csv')
nhanes_pedi = nhanes[nhanes['RIDAGEYR'] <= 13]
nhanes_pedi['SEQN'] = nhanes_pedi['SEQN'].astype(int)
patient_id_options = ['Select a patient OR input values below'] + sorted(nhanes_pedi['SEQN'].unique().tolist())
patient_id = st.selectbox('Select a patient (NHANES ID):', patient_id_options)

if patient_id == 'Select a patient OR input values below':
    # User inputs
    sex = st.radio('Select sex:', ('Male', 'Female'))
    age = st.slider('Select age (years):', min_value=0, max_value=13, value=10)
    height = st.number_input('Enter height (cm):', min_value=0, value=135)
    systolic_bp = st.number_input('Enter systolic blood pressure (mmHg):', min_value=0, value=100)
    diastolic_bp = st.number_input('Enter diastolic blood pressure (mmHg):', min_value=0, value=70)

    # Create a DataFrame for user inputs
    data = pd.DataFrame({
        'Age': [age for _ in range(2)],
        'Sex': [sex[0] for _ in range(2)],  # Use 'M' or 'F'
        'Height': [height for _ in range(2)],
        'Blood Pressure Value': [systolic_bp, diastolic_bp],
        'Type': ['Systolic BP', 'Diastolic BP']
    })

else:
    # Process NHANES data for selected patient
    nhanes_pt = nhanes_pedi[nhanes_pedi['SEQN'] == patient_id].iloc[0]
    data = pd.DataFrame({
        'Age': [nhanes_pt['RIDAGEYR'] for _ in range(2)],
        'Sex': ['M' if nhanes_pt['RIAGENDR'] == 1 else 'F' for _ in range(2)],
        'Height': [nhanes_pt['BMXHT'] for _ in range(2)],
        'Blood Pressure Value': [nhanes_pt['BPXSY1'], nhanes_pt['BPXDI1']],
        'Type': ['Systolic BP', 'Diastolic BP']
    })

# Calculate percentiles for either user input or NHANES data
for index, row in data.iterrows():
    # Select the correct BP table based on sex and type
    pertable = {
        ('M', 'Systolic BP'): pertable_ms,
        ('M', 'Diastolic BP'): pertable_md,
        ('F', 'Systolic BP'): pertable_fs,
        ('F', 'Diastolic BP'): pertable_fd,
    }[(row['Sex'], row['Type'])]

    # Find the closest age and height in the table
    current_pertable = pertable[pertable['Age (y)'] == round(row['Age'])]
    hts = current_pertable[current_pertable['Data'] == 'Height (cm)']
    hts = hts.iloc[:,2:]
    ht_col = abs(hts - row['Height']).stack().idxmin()[1]

    # Calculate the percentile
    bp_50 = current_pertable[current_pertable['Data'] == '50th'][ht_col].item()
    bp_95 = current_pertable[current_pertable['Data'] == '95th'][ht_col].item()
    bp_perc = calc_percentile(row['Blood Pressure Value'], bp_50, bp_95)
    data.at[index, 'Percentile'] = bp_perc

   # Label the percentile
    bp_label = ''
    if bp_perc <= 90:
        bp_label = 'Normal BP'
    elif bp_perc <= 95:
        bp_label = 'Elevated BP'
    else:
        bp_label = 'Hypertension'
    data.at[index, 'Blood Pressure Status'] = bp_label

# Tooltip
tooltip_content = [
    alt.Tooltip('Type:N', title='Type'),
    alt.Tooltip('Blood Pressure Value:Q', title='Value'),  # Correctly reference BP values
    alt.Tooltip('Percentile:Q', title='Percentile', format='.0f'),
    alt.Tooltip('Blood Pressure Status:N', title='Status'),
]

# Define horizontal lines for the 50th, 90th, and 95th percentiles
percentiles_df = pd.DataFrame({
    'Percentile': [50, 90, 95],
    'Label': ['50th', '90th', '95th']
})

# Adjusted definition for percentile lines without tooltip encoding
percentile_lines = alt.Chart(percentiles_df).mark_rule(color='black', size=1.5).encode(
    y='Percentile:Q'
).properties(
    tooltip=None  # This attempts to disable tooltips, but Altair might not directly support this property here.
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
data['Color'] = data['Percentile'].apply(lambda x: 'red' if x >= 95 else ('darkgoldenrod' if x >= 90 else 'darkgreen'))

# Keep your points definition as is, where tooltips are properly defined
points = alt.Chart(data).mark_point(
    filled=True,
    size=100
).encode(
    x=alt.X('Age:Q', title='Age (years)', axis=alt.Axis(values=list(range(14))), scale=alt.Scale(domain=(0, 13))),
    y=alt.Y('Percentile:Q', title='Blood Pressure Percentile', scale=alt.Scale(domain=(0, 100))),
    color=alt.Color('Color:N', legend=alt.Legend(title='Percentile Color'), scale=None),
    tooltip=tooltip_content  # Tooltips are applied here as intended
)

# Combine all chart layers without applying global tooltips
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
| **Normal BP (<90th percentile)** | - No additional action is needed<br>- BP should be rechecked at the next routine well-child care visit |
| **Elevated BP (≥90th to <95th percentile)** | - Lifestyle interventions (nutrition, sleep, physical activity) should be initiated<br>- BP should be rechecked by auscultatory measurement in 6 months<br>- If BP remains elevated at 6 months, check upper and lower extremity BP and repeat lifestyle measures<br>- If BP is still elevated after 12 months from initial measurement, order ambulatory blood pressure monitoring along with diagnostic evaluation, and consider subspecialty referral |
| **Hypertension (≥95th percentile)** |- If symptomatic, refer to emergency department immediately for evaluation and treatment <br>- If asymptomatic, initiate lifestyle interventions<br>- BP should be rechecked by auscultatory measurement in 1-2 weeks<br>- If it remains classified as hypertension at 1-2 weeks, check upper and lower extremity BP, and recheck BP in 3 months by auscultation with consideration for nutrition/weight management referral<br>- If BP continues to be classified as hypertension after 3 visits, order ambulatory blood pressure monitoring along with diagnostic evaluation, and initiate treatment with consideration for subspecialty referral |
""", unsafe_allow_html=True)    