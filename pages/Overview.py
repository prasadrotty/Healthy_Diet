import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Overview Dashboard",
    page_icon="🥗",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("healthy_diet_calorie_intake.csv")

df = load_data()

st.title("🥗 Healthy Diet Analytics Dashboard")
st.markdown("### Executive Overview")

st.divider()

# -----------------------------
# KPI SECTION
# -----------------------------
total_people = len(df)

avg_bmi = round(df["BMI"].mean(), 2)

avg_calories = round(
    df["Daily_Calorie_Consumed"].mean(), 0
)

avg_required = round(
    df["Daily_Calorie_Requirement"].mean(), 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Total Participants",
    total_people
)

col2.metric(
    "⚖ Average BMI",
    avg_bmi
)

col3.metric(
    "🔥 Avg Calories Consumed",
    avg_calories
)

col4.metric(
    "🎯 Avg Calories Required",
    avg_required
)

st.divider()

# -----------------------------
# ROW 1
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    health_counts = (
        df["Health_Status"]
        .value_counts()
        .reset_index()
    )

    fig = px.pie(
        health_counts,
        names="Health_Status",
        values="count",
        title="Health Status Distribution",
        hole=0.4
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    gender_counts = (
        df["Gender"]
        .value_counts()
        .reset_index()
    )

    fig = px.bar(
        gender_counts,
        x="Gender",
        y="count",
        title="Gender Distribution",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -----------------------------
# ROW 2
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        df,
        x="BMI",
        nbins=30,
        color="Gender",
        title="BMI Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

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

# -----------------------------
# ROW 3
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    diet_count = (
        df["Diet_Type"]
        .value_counts()
        .reset_index()
    )

    fig = px.bar(
        diet_count,
        x="Diet_Type",
        y="count",
        title="Diet Type Distribution",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        df,
        x="Activity_Level",
        y="Daily_Calorie_Consumed",
        color="Activity_Level",
        title="Calories Consumed by Activity Level"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -----------------------------
# CALORIE ANALYSIS
# -----------------------------
st.subheader("🔥 Calorie Analytics")

fig = px.scatter(
    df,
    x="Daily_Calorie_Requirement",
    y="Daily_Calorie_Consumed",
    color="Health_Status",
    size="BMI",
    hover_data=["Gender"],
    title="Calories Required vs Consumed"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -----------------------------
# WATER INTAKE ANALYSIS
# -----------------------------
if "Water_Intake_Liters" in df.columns:

    st.subheader("💧 Water Intake Analysis")

    fig = px.box(
        df,
        x="Health_Status",
        y="Water_Intake_Liters",
        color="Health_Status",
        title="Water Intake by Health Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -----------------------------
# AI GENERATED INSIGHTS
# -----------------------------
st.subheader("🤖 Smart Insights")

avg_bmi = df["BMI"].mean()

avg_consume = df[
    "Daily_Calorie_Consumed"
].mean()

avg_required = df[
    "Daily_Calorie_Requirement"
].mean()

top_diet = (
    df["Diet_Type"]
    .value_counts()
    .idxmax()
)

top_health = (
    df["Health_Status"]
    .value_counts()
    .idxmax()
)

if avg_bmi > 25:
    st.warning(
        f"Average BMI is {avg_bmi:.2f}. Population tends toward overweight category."
    )
else:
    st.success(
        f"Average BMI is {avg_bmi:.2f}. Population is within healthy range."
    )

if avg_consume > avg_required:
    st.error(
        "Average calorie intake exceeds required calories. Potential calorie surplus detected."
    )
else:
    st.success(
        "Average calorie intake is within required limits."
    )

st.info(
    f"Most followed diet type: {top_diet}"
)

st.info(
    f"Dominant health category: {top_health}"
)

st.divider()

# -----------------------------
# RAW DATA
# -----------------------------
with st.expander("📊 View Dataset"):
    st.dataframe(
        df,
        use_container_width=True
    )

st.caption(
    "Healthy Diet & Nutrition Analytics Dashboard | Built using Streamlit & Plotly"
)
