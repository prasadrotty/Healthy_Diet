import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Nutrition Analysis",
    page_icon="🥗",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("healthy_diet_calorie_intake.csv")

df = load_data()

st.title("🥗 Nutrition Analysis Dashboard")
st.markdown("### Deep Nutritional Insights")

st.divider()

# -------------------------------------------------
# COLUMN VALIDATION
# -------------------------------------------------
required_cols = [
    "Protein_Intake_g",
    "Carbohydrate_Intake_g",
    "Fat_Intake_g"
]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(
        f"Missing columns in dataset: {missing}"
    )
    st.stop()

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
avg_protein = round(
    df["Protein_Intake_g"].mean(), 2
)

avg_carbs = round(
    df["Carbohydrate_Intake_g"].mean(), 2
)

avg_fat = round(
    df["Fat_Intake_g"].mean(), 2
)

avg_calories = round(
    df["Daily_Calorie_Consumed"].mean(), 2
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🥩 Avg Protein (g)",
    avg_protein
)

col2.metric(
    "🍞 Avg Carbs (g)",
    avg_carbs
)

col3.metric(
    "🥑 Avg Fat (g)",
    avg_fat
)

col4.metric(
    "🔥 Avg Calories",
    avg_calories
)

st.divider()

# -------------------------------------------------
# MACRONUTRIENT DISTRIBUTION
# -------------------------------------------------
st.subheader("📊 Macronutrient Distribution")

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        df,
        x="Protein_Intake_g",
        nbins=25,
        title="Protein Intake Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.histogram(
        df,
        x="Carbohydrate_Intake_g",
        nbins=25,
        title="Carbohydrate Intake Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -------------------------------------------------
# FAT DISTRIBUTION
# -------------------------------------------------
fig = px.histogram(
    df,
    x="Fat_Intake_g",
    nbins=25,
    title="Fat Intake Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# MACRO COMPOSITION
# -------------------------------------------------
st.subheader("🥗 Average Macronutrient Composition")

macro_df = pd.DataFrame(
    {
        "Nutrient": [
            "Protein",
            "Carbohydrates",
            "Fat"
        ],
        "Value": [
            avg_protein,
            avg_carbs,
            avg_fat
        ]
    }
)

fig = px.pie(
    macro_df,
    names="Nutrient",
    values="Value",
    hole=0.45,
    title="Average Macronutrient Split"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# DIET TYPE ANALYSIS
# -------------------------------------------------
if "Diet_Type" in df.columns:

    st.subheader("🥬 Nutrition by Diet Type")

    diet_summary = (
        df.groupby("Diet_Type")[
            [
                "Protein_Intake_g",
                "Carbohydrate_Intake_g",
                "Fat_Intake_g"
            ]
        ]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        diet_summary,
        x="Diet_Type",
        y=[
            "Protein_Intake_g",
            "Carbohydrate_Intake_g",
            "Fat_Intake_g"
        ],
        barmode="group",
        title="Average Nutrition by Diet Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -------------------------------------------------
# ACTIVITY LEVEL ANALYSIS
# -------------------------------------------------
if "Activity_Level" in df.columns:

    st.subheader("🏃 Nutrition by Activity Level")

    fig = px.box(
        df,
        x="Activity_Level",
        y="Protein_Intake_g",
        color="Activity_Level",
        title="Protein Intake by Activity Level"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -------------------------------------------------
# CORRELATION HEATMAP
# -------------------------------------------------
st.subheader("📈 Nutrition Correlation Analysis")

numeric_cols = [
    "Protein_Intake_g",
    "Carbohydrate_Intake_g",
    "Fat_Intake_g",
    "Daily_Calorie_Consumed",
    "Daily_Calorie_Requirement",
    "BMI"
]

available_cols = [
    col for col in numeric_cols
    if col in df.columns
]

corr = df[available_cols].corr()

fig = ff.create_annotated_heatmap(
    z=np.round(corr.values, 2),
    x=list(corr.columns),
    y=list(corr.index),
    annotation_text=np.round(
        corr.values, 2
    ),
    showscale=True
)

fig.update_layout(
    height=650,
    title="Correlation Heatmap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# BMI VS NUTRITION
# -------------------------------------------------
st.subheader("⚖ BMI vs Nutrition")

fig = px.scatter(
    df,
    x="Protein_Intake_g",
    y="BMI",
    color="Health_Status"
    if "Health_Status" in df.columns
    else None,
    title="Protein Intake vs BMI"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# CALORIES VS MACROS
# -------------------------------------------------
st.subheader("🔥 Calories vs Macronutrients")

fig = px.scatter(
    df,
    x="Carbohydrate_Intake_g",
    y="Daily_Calorie_Consumed",
    color="Fat_Intake_g",
    size="Protein_Intake_g",
    title="Calories vs Macronutrients"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# AI GENERATED INSIGHTS
# -------------------------------------------------
st.subheader("🤖 AI Nutrition Insights")

highest_macro = max(
    {
        "Protein": avg_protein,
        "Carbohydrates": avg_carbs,
        "Fat": avg_fat
    },
    key=lambda x: {
        "Protein": avg_protein,
        "Carbohydrates": avg_carbs,
        "Fat": avg_fat
    }[x]
)

st.info(
    f"Highest average nutrient intake is {highest_macro}."
)

if avg_protein < 60:
    st.warning(
        "Average protein intake is relatively low."
    )
else:
    st.success(
        "Protein intake appears adequate."
    )

if avg_fat > avg_protein:
    st.warning(
        "Fat consumption is higher than protein intake."
    )

if avg_carbs > 200:
    st.info(
        "Population shows a carbohydrate-rich diet pattern."
    )

if (
    "Daily_Calorie_Consumed" in df.columns
    and
    "Daily_Calorie_Requirement" in df.columns
):
    surplus = (
        df["Daily_Calorie_Consumed"].mean()
        -
        df["Daily_Calorie_Requirement"].mean()
    )

    if surplus > 0:
        st.error(
            f"Average calorie surplus detected ({surplus:.2f} kcal)."
        )
    else:
        st.success(
            "Average calorie intake is within requirement."
        )

st.divider()

# -------------------------------------------------
# RAW DATA
# -------------------------------------------------
with st.expander(
    "📋 View Nutrition Dataset"
):
    st.dataframe(
        df,
        use_container_width=True
    )

st.caption(
    "Nutrition Analytics Dashboard | Streamlit + Plotly"
)
