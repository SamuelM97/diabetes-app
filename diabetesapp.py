# app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Diabetes EDA", layout="centered")

# Title and intro
st.title("Exploring Diabetes Risk Factors")
st.write("""
This app provides an interactive overview of diabetes trends in the Pima Indians Diabetes Dataset.
Use the controls to explore key visual insights across age groups, BMI categories, and more.
""")

# Load data
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1Y5i5PHmZ28MmTEVnTBFQzJHW880HfF-2"
    df = pd.read_csv(url)
    df['AgeGroup'] = pd.cut(df['Age'], bins=[20, 30, 40, 50, 60, 100], labels=['20s', '30s', '40s', '50s', '60+'])
    df['BMICategory'] = pd.cut(df['BMI'], bins=[0, 18.5, 24.9, 29.9, 34.9, 100],
                               labels=['Underweight', 'Normal', 'Overweight', 'Obese I', 'Obese II+'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
age_group = st.sidebar.selectbox("Select Age Group", df['AgeGroup'].cat.categories)
bmi_group = st.sidebar.selectbox("Select BMI Category", df['BMICategory'].cat.categories)

# Filtered subset
subset = df[(df['AgeGroup'] == age_group) & (df['BMICategory'] == bmi_group)]

# Show filtered subset
st.subheader(f"Patients in Age Group {age_group} and BMI Group {bmi_group}")
st.write(f"Number of patients: {subset.shape[0]}")
st.dataframe(subset)

# Plot: Diabetes Rate by Age Group
st.subheader("Diabetes Rate by Age Group")
fig1, ax1 = plt.subplots()
sns.pointplot(data=df, x='AgeGroup', y='Outcome', errorbar='sd', ax=ax1)
ax1.set_title("Diabetes Rate by Age Group")
st.pyplot(fig1)

# Plot: Diabetes Rate by BMI Category
st.subheader("Diabetes Rate by BMI Category")
fig2, ax2 = plt.subplots()
sns.pointplot(data=df, x='BMICategory', y='Outcome', errorbar='sd', ax=ax2)
ax2.set_title("Diabetes Rate by BMI Category")
st.pyplot(fig2)
