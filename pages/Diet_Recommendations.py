import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Diet Recommendations",
    page_icon="🥗",
    layout="wide"
)

# -----------------------------------
# LOAD DATA
# -----------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("healthy_diet_calorie_intake.csv")

df = load_data()

st.title("🥗 Diet Recommendation Engine")
st.markdown("### Personalized Nutrition & Health Suggestions")

st.divider()

# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------
st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Select Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

activity = st.sidebar.multiselect(
    "Activity Level",
    df["Activity_Level"].unique(),
    default=df["Activity_Level"].unique()
)

filtered_df = df[
    (df["Gender"].isin(gender)) &
    (df["Activity_Level"].isin(activity))
]

# -----------------------------------
# BMI CLASSIFICATION
# -----------------------------------
def bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"

filtered_df["BMI_Category"] = (
    filtered_df["BMI"]
    .apply(bmi_category)
)

# -----------------------------------
# KPI SECTION
# -----------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "People",
    len(filtered_df)
)

col2.metric(
    "Average BMI",
    round(filtered_df["BMI"].mean(), 2)
)

col3.metric(
    "Avg Calories Consumed",
    round(
        filtered_df[
            "Daily_Calorie_Consumed"
        ].mean(),
        0
    )
)

col4.metric(
    "Avg Calories Required",
    round(
        filtered_df[
            "Daily_Calorie_Requirement"
        ].mean(),
        0
    )
)

st.divider()

# -----------------------------------
# BMI CATEGORY DISTRIBUTION
# -----------------------------------
st.subheader("BMI Category Distribution")

bmi_counts = (
    filtered_df["BMI_Category"]
    .value_counts()
    .reset_index()
)

fig = px.pie(
    bmi_counts,
    names="BMI_Category",
    values="count",
    hole=0.4
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -----------------------------------
# CALORIE BALANCE
# -----------------------------------
filtered_df["Calorie_Balance"] = (
    filtered_df["Daily_Calorie_Consumed"]
    -
    filtered_df["Daily_Calorie_Requirement"]
)

st.subheader("Calorie Surplus / Deficit")

fig = px.histogram(
    filtered_df,
    x="Calorie_Balance",
    nbins=30,
    title="Calorie Balance Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -----------------------------------
# DIET TYPE ANALYSIS
# -----------------------------------
if "Diet_Type" in filtered_df.columns:

    st.subheader("Diet Type Distribution")

    diet_df = (
        filtered_df["Diet_Type"]
        .value_counts()
        .reset_index()
    )

    fig = px.bar(
        diet_df,
        x="Diet_Type",
        y="count",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -----------------------------------
# RECOMMENDATION ENGINE
# -----------------------------------
st.subheader("🥗 Health Recommendations")

avg_bmi = filtered_df["BMI"].mean()

avg_balance = (
    filtered_df["Calorie_Balance"]
    .mean()
)

if avg_bmi < 18.5:

    st.warning("""
    ### Underweight Population

    Recommendations:
    - Increase calorie intake
    - Add healthy fats
    - Increase protein intake
    - Strength training exercises
    - Eat frequent meals
    """)

elif avg_bmi < 25:

    st.success("""
    ### Healthy BMI Population

    Recommendations:
    - Maintain current eating habits
    - Continue regular exercise
    - Ensure balanced nutrition
    - Stay hydrated
    """)

elif avg_bmi < 30:

    st.warning("""
    ### Overweight Population

    Recommendations:
    - Moderate calorie deficit
    - Increase physical activity
    - Reduce processed foods
    - Increase vegetables and protein
    """)

else:

    st.error("""
    ### Obese Population

    Recommendations:
    - Structured weight-loss plan
    - Nutrition monitoring
    - Daily exercise routine
    - Reduce sugary foods
    - Consult healthcare professionals
    """)

st.divider()

# -----------------------------------
# CALORIE RECOMMENDATIONS
# -----------------------------------
st.subheader("🔥 Calorie Insights")

if avg_balance > 200:

    st.error(
        f"Average calorie surplus detected ({avg_balance:.0f} kcal)."
    )

    st.write("""
    Suggestions:
    - Reduce calorie-dense snacks
    - Increase physical activity
    - Monitor portion sizes
    """)

elif avg_balance < -200:

    st.warning(
        f"Average calorie deficit detected ({abs(avg_balance):.0f} kcal)."
    )

    st.write("""
    Suggestions:
    - Increase nutrient-rich foods
    - Add healthy snacks
    - Improve protein intake
    """)

else:

    st.success(
        "Calorie consumption is close to requirement."
    )

st.divider()

# -----------------------------------
# PROTEIN ANALYSIS
# -----------------------------------
if "Protein_Intake_g" in filtered_df.columns:

    avg_protein = (
        filtered_df[
            "Protein_Intake_g"
        ].mean()
    )

    st.subheader("🥩 Protein Recommendations")

    if avg_protein < 60:

        st.warning(
            f"Average protein intake is only {avg_protein:.1f} g."
        )

        st.write("""
        Recommended Sources:
        - Eggs
        - Chicken
        - Fish
        - Paneer
        - Lentils
        - Soy products
        """)

    else:

        st.success(
            f"Protein intake appears adequate ({avg_protein:.1f} g)."
        )

st.divider()

# -----------------------------------
# ACTIVITY LEVEL INSIGHTS
# -----------------------------------
if "Activity_Level" in filtered_df.columns:

    st.subheader("🏃 Activity Level Analysis")

    activity_summary = (
        filtered_df.groupby(
            "Activity_Level"
        )[
            "Daily_Calorie_Consumed"
        ]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        activity_summary,
        x="Activity_Level",
        y="Daily_Calorie_Consumed",
        title="Average Calories by Activity Level",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -----------------------------------
# AI INSIGHTS
# -----------------------------------
st.subheader("🤖 AI Generated Insights")

top_bmi = (
    filtered_df["BMI_Category"]
    .value_counts()
    .idxmax()
)

top_diet = (
    filtered_df["Diet_Type"]
    .value_counts()
    .idxmax()
)

st.info(
    f"Most common BMI category: {top_bmi}"
)

st.info(
    f"Most followed diet type: {top_diet}"
)

st.info(
    f"Average BMI of selected population: {avg_bmi:.2f}"
)

st.info(
    f"Average calorie balance: {avg_balance:.2f} kcal"
)

st.divider()

# -----------------------------------
# DATA VIEW
# -----------------------------------
with st.expander("View Filtered Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

st.caption(
    "Diet Recommendation Engine | Streamlit Analytics Project"
)
