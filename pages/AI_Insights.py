import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("healthy_diet_calorie_intake.csv")

df = load_data()

st.title("🤖 AI Health Insights Dashboard")
st.markdown("### Machine Learning & Advanced Analytics")

st.divider()

# -------------------------------------------------
# HEALTH RISK SCORE
# -------------------------------------------------

st.subheader("⚠️ Health Risk Score")

def calculate_risk(row):

    score = 0

    if row["BMI"] >= 30:
        score += 40

    elif row["BMI"] >= 25:
        score += 20

    calorie_gap = abs(
        row["Daily_Calorie_Consumed"]
        -
        row["Daily_Calorie_Requirement"]
    )

    if calorie_gap > 500:
        score += 30

    elif calorie_gap > 250:
        score += 15

    if "Water_Intake_Liters" in df.columns:

        if row["Water_Intake_Liters"] < 2:
            score += 10

    return score

df["Risk_Score"] = df.apply(
    calculate_risk,
    axis=1
)

avg_risk = round(
    df["Risk_Score"].mean(),
    2
)

st.metric(
    "Average Health Risk Score",
    avg_risk
)

fig = px.histogram(
    df,
    x="Risk_Score",
    nbins=20,
    title="Health Risk Score Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# RISK CATEGORY
# -------------------------------------------------

def risk_category(score):

    if score < 20:
        return "Low Risk"

    elif score < 50:
        return "Medium Risk"

    else:
        return "High Risk"

df["Risk_Category"] = df[
    "Risk_Score"
].apply(risk_category)

risk_df = (
    df["Risk_Category"]
    .value_counts()
    .reset_index()
)

fig = px.pie(
    risk_df,
    names="Risk_Category",
    values="count",
    hole=0.4,
    title="Population Risk Categories"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# KMEANS SEGMENTATION
# -------------------------------------------------

st.subheader("🧠 AI Population Segmentation")

features = [
    "BMI",
    "Daily_Calorie_Consumed",
    "Daily_Calorie_Requirement"
]

if "Protein_Intake_g" in df.columns:
    features.append("Protein_Intake_g")

cluster_df = df[features].copy()

scaler = StandardScaler()

scaled_data = scaler.fit_transform(
    cluster_df
)

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(
    scaled_data
)

fig = px.scatter(
    df,
    x="BMI",
    y="Daily_Calorie_Consumed",
    color="Cluster",
    title="AI Population Segments"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# CLUSTER SUMMARY
# -------------------------------------------------

st.subheader("Cluster Analysis")

cluster_summary = (
    df.groupby("Cluster")[
        features
    ]
    .mean()
    .round(2)
)

st.dataframe(
    cluster_summary,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# BMI PREDICTION MODEL
# -------------------------------------------------

st.subheader("📈 BMI Prediction Model")

predictors = [
    "Daily_Calorie_Consumed",
    "Daily_Calorie_Requirement"
]

if "Protein_Intake_g" in df.columns:
    predictors.append(
        "Protein_Intake_g"
    )

X = df[predictors]

y = df["BMI"]

model = LinearRegression()

model.fit(X, y)

predictions = model.predict(X)

df["Predicted_BMI"] = predictions

fig = px.scatter(
    x=y,
    y=predictions,
    labels={
        "x": "Actual BMI",
        "y": "Predicted BMI"
    },
    title="Actual vs Predicted BMI"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# FEATURE IMPORTANCE
# -------------------------------------------------

st.subheader("🔍 BMI Drivers")

importance_df = pd.DataFrame(
    {
        "Feature": predictors,
        "Coefficient": model.coef_
    }
)

importance_df = importance_df.sort_values(
    by="Coefficient",
    ascending=False
)

fig = px.bar(
    importance_df,
    x="Feature",
    y="Coefficient",
    title="Factors Influencing BMI"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# EXECUTIVE SUMMARY
# -------------------------------------------------

st.subheader("📋 Executive Summary")

avg_bmi = round(
    df["BMI"].mean(),
    2
)

avg_calories = round(
    df["Daily_Calorie_Consumed"].mean(),
    0
)

avg_required = round(
    df["Daily_Calorie_Requirement"].mean(),
    0
)

top_risk = (
    df["Risk_Category"]
    .value_counts()
    .idxmax()
)

summary = f"""
Total Records: {len(df)}

Average BMI: {avg_bmi}

Average Calories Consumed: {avg_calories}

Average Calories Required: {avg_required}

Dominant Risk Category: {top_risk}

AI identified 4 unique population clusters.

BMI prediction model successfully trained.
"""

st.success(summary)

st.divider()

# -------------------------------------------------
# DOWNLOAD REPORT
# -------------------------------------------------

st.subheader("📥 Download AI Insights")

report_df = df[
    [
        "BMI",
        "Risk_Score",
        "Risk_Category",
        "Cluster",
        "Predicted_BMI"
    ]
]

csv = report_df.to_csv(
    index=False
)

st.download_button(
    label="Download AI Report",
    data=csv,
    file_name="ai_health_insights.csv",
    mime="text/csv"
)

st.divider()

# -------------------------------------------------
# DATA PREVIEW
# -------------------------------------------------

with st.expander(
    "View AI Processed Data"
):
    st.dataframe(
        df.head(100),
        use_container_width=True
    )

st.caption(
    "AI Health Insights Dashboard | Machine Learning + Streamlit"
)
