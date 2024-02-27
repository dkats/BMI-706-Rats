import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###
@st.cache_data
def load_data():
    cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(
        id_vars=["Country", "Year", "Cancer", "Sex"], 
        var_name="Age", 
        value_name="Deaths"
    )
    
    pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(
        id_vars=["Country", "Year", "Sex"], 
        var_name="Age", 
        value_name="Pop"
    )
    
    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)
    
    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000
    
    return df

df = load_data()

st.write("## Age-specific cancer mortality rates")

### P2.1 ###
min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
year = st.slider('Select a year', min_value=min_year, max_value=max_year, value=min_year)
subset = df[df["Year"] == year]

### P2.2 ###
sex = ['M', 'F']
sex_selection = st.radio('Select sex:', options=sex, index=0)
subset = subset[subset["Sex"] == sex_selection]

### P2.3 ###
countries = [
    "Austria",
    "Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand",
    "Turkey",
]

countries_selection = st.multiselect(
    'Select countries:',
    options=countries,
    default=countries
)

subset = subset[subset["Country"].isin(countries_selection)]

### P2.4 ###
cancer = st.selectbox('Cancer', sorted(set(df['Cancer'])))
subset = subset[subset["Cancer"] == cancer]

### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

### PBonus ###
age_selection = alt.selection_interval(encodings=['x'])
### PBonus ###

chart = alt.Chart(subset).mark_rect().encode(
    x=alt.X("Age:O", sort=ages),
    y=alt.Y('Country:N', sort='ascending'),
    color=alt.Color("Rate:Q", title="Mortality rate per 100k", scale=alt.Scale(type='log', domain=(0.01, 1000), clamp=True)),
    tooltip=["Rate:Q"],
).properties(
    title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
    width=500
).add_selection(
    age_selection
)
### P2.5 ###

st.altair_chart(chart, use_container_width=True)

### PBonus ###
#chart_bonus = alt.Chart(subset).mark_bar().encode(
#    x=alt.X("sum(Pop):Q", title='Sum of population size'),
#    y=alt.Y('Country:N', sort='-x'),
#).properties(
#    width=500
#).transform_filter(
#    age_selection
#)

#st.altair_chart(chart_bonus, use_container_width=True)
#st.altair_chart(alt.vconcat(chart, chart_bonus), use_container_width=True)
### PBonus ###

countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")