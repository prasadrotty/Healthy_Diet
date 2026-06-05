import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Healthy Diet Analytics",
    page_icon="🥗",
    layout="wide"
)

# Load Data
df = pd.read_csv("healthy_diet_calorie_intake.csv")

st.title("🥗 Healthy Diet & Calorie Analytics Dashboard")

# KPI Metrics
col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Participants",
    len(df)
)

col2.metric(
    "Average BMI",
    round(df["BMI"].mean(),2)
)

col3.metric(
    "Calories Consumed",
    round(df["Daily_Calorie_Consumed"].mean(),0)
)

col4.metric(
    "Calories Required",
    round(df["Daily_Calorie_Requirement"].mean(),0)
)

st.divider()

# Health Status
fig = px.pie(
    df,
    names="Health_Status",
    title="Health Status Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# BMI Distribution
fig2 = px.histogram(
    df,
    x="BMI",
    color="Gender",
    nbins=30,
    title="BMI Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# Calorie Requirement vs Consumption
fig3 = px.scatter(
    df,
    x="Daily_Calorie_Requirement",
    y="Daily_Calorie_Consumed",
    color="Health_Status",
    title="Calories Required vs Consumed"
)

st.plotly_chart(fig3, use_container_width=True)

# Diet Type Distribution
fig4 = px.bar(
    df["Diet_Type"].value_counts().reset_index(),
    x="Diet_Type",
    y="count",
    title="Diet Type Distribution"
)

st.plotly_chart(fig4, use_container_width=True)

# Activity Level
fig5 = px.box(
    df,
    x="Activity_Level",
    y="Daily_Calorie_Consumed",
    color="Gender",
    title="Calories by Activity Level"
)

st.plotly_chart(fig5, use_container_width=True)

st.divider()

# AI Insights
st.subheader("🤖 AI Generated Insights")

avg_bmi = df["BMI"].mean()

avg_req = df["Daily_Calorie_Requirement"].mean()
avg_con = df["Daily_Calorie_Consumed"].mean()

if avg_bmi > 25:
    st.warning(
        f"Average BMI is {avg_bmi:.2f}. Population leans toward overweight."
    )

if avg_con > avg_req:
    st.error(
        "Average calorie consumption exceeds requirement."
    )
else:
    st.success(
        "Population maintains calorie balance."
    )

top_diet = df["Diet_Type"].mode()[0]

st.info(
    f"Most common diet pattern: {top_diet}"
)
