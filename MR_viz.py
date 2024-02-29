import altair as alt
import pandas as pd
import streamlit as st
import xport    # Needed for XPT import
import types    # Needed for @st.cache(hash_funcs={types.FunctionType: lambda _: None})

### NHANES import
@st.cache_data(hash_funcs={types.FunctionType: lambda _: None})
def load_data_xpt(filename, columns_to_keep=None):
    with open(filename, 'rb') as f:
        df = pd.DataFrame(xport.to_dataframe(f))
        
        # If specific columns to keep have been specified, filter the DataFrame
        if columns_to_keep is not None:
            relevant_columns = [col for col in columns_to_keep if col in df.columns]
            df = df[relevant_columns]
        return df

# Load NHANES data
nhanes = pd.DataFrame()
f_body_measures = ['BMX_B.XPT','BMX_C.XPT','BMX_D.XPT','BMX_E.XPT','BMX_F.XPT','BMX_G.XPT','BMX_H.XPT','BMX_I.XPT','BMX_J.XPT','BMX.XPT','P_BMX.XPT']
f_blood_pressures = ['BPX_B.XPT','BPX_C.XPT','BPX_D.XPT','BPX_E.XPT','BPX_F.XPT','BPX_G.XPT','BPX_H.XPT','BPX_I.XPT','BPX_J.XPT','BPX.XPT','P_BPXO.XPT','BPXO_J.XPT']
f_demographics = ['DEMO_B.XPT','DEMO_C.XPT','DEMO_D.XPT','DEMO_E.XPT','DEMO_F.XPT','DEMO_G.XPT','DEMO_H.XPT','DEMO_I.XPT','DEMO_J.XPT','DEMO.XPT','P_DEMO.XPT']
for i in range(len(f_body_measures)):
    body_measures = load_data_xpt('nhanes/' + f_body_measures[i], ['SEQN', 'BMXWT', 'BMXHT'])    # Not including 'BMDSTATS' due to incomplete data
    blood_pressures = load_data_xpt('nhanes/' + f_blood_pressures[i], ['SEQN', 'BPXSY1', 'BPXDI1'])    # Not including 'BPXSY2', 'BPXDI2', 'BPXSY3', 'BPXDI3', 'BPXOSY1', 'BPXODI1', 'BPXOSY2', 'BPXODI2', 'BPXOSY3', 'BPXODI3' for simplicity
    demographics = load_data_xpt('nhanes/' + f_demographics[i], ['SEQN', 'RIAGENDR', 'RIDAGEYR', 'RIDAGEMN'])
    
    # Drop incomplete rows
    body_measures.dropna(inplace=True)
    demographics.dropna(inplace=True)
    skip = False
    if(len(blood_pressures.columns) == len(['SEQN', 'BPXSY1', 'BPXDI1'])):
        blood_pressures.dropna(inplace=True, subset=['BPXSY1', 'BPXDI1'], how='all')
    else:
        skip = True

    # Merge dataframes
    if(not skip):
        all = pd.merge(body_measures, demographics, on='SEQN', how='inner')
        all = pd.merge(all, blood_pressures, on='SEQN', how='inner')
        nhanes = pd.concat([nhanes, all], ignore_index=True)

nhanes['RIDAGEYR'] = nhanes['RIDAGEMN'] / 12


### Streamlit
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