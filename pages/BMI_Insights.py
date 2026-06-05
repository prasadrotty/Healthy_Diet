import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="BMI Insights",
    page_icon="⚖",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("healthy_diet_calorie_intake.csv")

df = load_data()

st.title("⚖ BMI Insights Dashboard")
st.markdown("### Body Mass Index & Health Risk Analytics")

st.divider()

# --------------------------------------------------
# CHECK BMI COLUMN
# --------------------------------------------------
if "BMI" not in df.columns:
    st.error("BMI column not found in dataset.")
    st.stop()

# --------------------------------------------------
# BMI CATEGORIES
# --------------------------------------------------
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

df["BMI_Category"] = df["BMI"].apply(bmi_category)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------
avg_bmi = round(df["BMI"].mean(), 2)

underweight = len(df[df["BMI_Category"] == "Underweight"])
normal = len(df[df["BMI_Category"] == "Normal"])
overweight = len(df[df["BMI_Category"] == "Overweight"])
obese = len(df[df["BMI_Category"] == "Obese"])

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Average BMI", avg_bmi)
col2.metric("Underweight", underweight)
col3.metric("Normal", normal)
col4.metric("Overweight", overweight)
col5.metric("Obese", obese)

st.divider()

# --------------------------------------------------
# BMI CATEGORY DISTRIBUTION
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    fig = px.pie(
        df,
        names="BMI_Category",
        title="BMI Category Distribution",
        hole=0.4
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:
    fig = px.histogram(
        df,
        x="BMI",
        nbins=30,
        title="BMI Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# BMI BY GENDER
# --------------------------------------------------
if "Gender" in df.columns:

    st.subheader("👨‍🦱 BMI by Gender")

    fig = px.box(
        df,
        x="Gender",
        y="BMI",
        color="Gender",
        title="BMI Comparison by Gender"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# BMI BY DIET TYPE
# --------------------------------------------------
if "Diet_Type" in df.columns:

    st.subheader("🥗 BMI by Diet Type")

    fig = px.box(
        df,
        x="Diet_Type",
        y="BMI",
        color="Diet_Type",
        title="BMI Distribution Across Diet Types"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# BMI VS CALORIES
# --------------------------------------------------
if (
    "Daily_Calorie_Consumed" in df.columns
):

    st.subheader("🔥 BMI vs Calories Consumed")

    fig = px.scatter(
        df,
        x="Daily_Calorie_Consumed",
        y="BMI",
        color="BMI_Category",
        title="Calories Consumed vs BMI"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# BMI VS ACTIVITY LEVEL
# --------------------------------------------------
if "Activity_Level" in df.columns:

    st.subheader("🏃 BMI by Activity Level")

    fig = px.box(
        df,
        x="Activity_Level",
        y="BMI",
        color="Activity_Level",
        title="BMI Across Activity Levels"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# HEALTH STATUS ANALYSIS
# --------------------------------------------------
if "Health_Status" in df.columns:

    st.subheader("❤️ BMI vs Health Status")

    fig = px.box(
        df,
        x="Health_Status",
        y="BMI",
        color="Health_Status",
        title="BMI Distribution by Health Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# BMI CATEGORY COUNT
# --------------------------------------------------
st.subheader("📊 BMI Risk Categories")

category_count = (
    df["BMI_Category"]
    .value_counts()
    .reset_index()
)

fig = px.bar(
    category_count,
    x="BMI_Category",
    y="count",
    color="BMI_Category",
    text_auto=True,
    title="BMI Category Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------
st.subheader("🤖 AI Generated BMI Insights")

highest_group = (
    df["BMI_Category"]
    .value_counts()
    .idxmax()
)

st.info(
    f"Most individuals belong to the '{highest_group}' BMI category."
)

if avg_bmi < 18.5:
    st.warning(
        "Population average BMI indicates underweight trend."
    )

elif avg_bmi < 25:
    st.success(
        "Population average BMI is within healthy range."
    )

elif avg_bmi < 30:
    st.warning(
        "Population average BMI indicates overweight trend."
    )

else:
    st.error(
        "Population average BMI indicates obesity risk."
    )

obesity_rate = round(
    (obese / len(df)) * 100,
    2
)

st.info(
    f"Obesity prevalence in dataset: {obesity_rate}%"
)

st.divider()

# --------------------------------------------------
# DATA EXPLORER
# --------------------------------------------------
with st.expander("📋 View BMI Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )

st.caption(
    "BMI Insights Dashboard | Streamlit + Plotly"
)
