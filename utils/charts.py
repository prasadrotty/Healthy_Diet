import plotly.express as px
import plotly.figure_factory as ff
import numpy as np


# --------------------------------------------------
# HEALTH STATUS PIE CHART
# --------------------------------------------------

def health_status_chart(df):

    health_df = (
        df["Health_Status"]
        .value_counts()
        .reset_index()
    )

    fig = px.pie(
        health_df,
        names="Health_Status",
        values="count",
        hole=0.4,
        title="Health Status Distribution"
    )

    return fig


# --------------------------------------------------
# BMI DISTRIBUTION
# --------------------------------------------------

def bmi_distribution_chart(df):

    fig = px.histogram(
        df,
        x="BMI",
        color="Gender",
        nbins=30,
        title="BMI Distribution"
    )

    return fig


# --------------------------------------------------
# GENDER DISTRIBUTION
# --------------------------------------------------

def gender_distribution_chart(df):

    gender_df = (
        df["Gender"]
        .value_counts()
        .reset_index()
    )

    fig = px.bar(
        gender_df,
        x="Gender",
        y="count",
        text_auto=True,
        title="Gender Distribution"
    )

    return fig


# --------------------------------------------------
# DIET TYPE DISTRIBUTION
# --------------------------------------------------

def diet_distribution_chart(df):

    diet_df = (
        df["Diet_Type"]
        .value_counts()
        .reset_index()
    )

    fig = px.bar(
        diet_df,
        x="Diet_Type",
        y="count",
        text_auto=True,
        title="Diet Type Distribution"
    )

    return fig


# --------------------------------------------------
# BMI BY GENDER
# --------------------------------------------------

def bmi_gender_chart(df):

    fig = px.box(
        df,
        x="Gender",
        y="BMI",
        color="Gender",
        title="BMI Comparison by Gender"
    )

    return fig


# --------------------------------------------------
# CALORIES VS REQUIREMENT
# --------------------------------------------------

def calorie_scatter_chart(df):

    fig = px.scatter(
        df,
        x="Daily_Calorie_Requirement",
        y="Daily_Calorie_Consumed",
        color="Health_Status",
        size="BMI",
        title="Calories Required vs Consumed"
    )

    return fig


# --------------------------------------------------
# ACTIVITY LEVEL CALORIES
# --------------------------------------------------

def activity_calorie_chart(df):

    fig = px.box(
        df,
        x="Activity_Level",
        y="Daily_Calorie_Consumed",
        color="Activity_Level",
        title="Calories by Activity Level"
    )

    return fig


# --------------------------------------------------
# PROTEIN DISTRIBUTION
# --------------------------------------------------

def protein_chart(df):

    fig = px.histogram(
        df,
        x="Protein_Intake_g",
        nbins=25,
        title="Protein Intake Distribution"
    )

    return fig


# --------------------------------------------------
# CARBOHYDRATE DISTRIBUTION
# --------------------------------------------------

def carbs_chart(df):

    fig = px.histogram(
        df,
        x="Carbohydrate_Intake_g",
        nbins=25,
        title="Carbohydrate Intake Distribution"
    )

    return fig


# --------------------------------------------------
# FAT DISTRIBUTION
# --------------------------------------------------

def fat_chart(df):

    fig = px.histogram(
        df,
        x="Fat_Intake_g",
        nbins=25,
        title="Fat Intake Distribution"
    )

    return fig


# --------------------------------------------------
# MACRO SPLIT PIE CHART
# --------------------------------------------------

def macro_split_chart(df):

    protein = df["Protein_Intake_g"].mean()
    carbs = df["Carbohydrate_Intake_g"].mean()
    fat = df["Fat_Intake_g"].mean()

    macro_data = {
        "Nutrient": [
            "Protein",
            "Carbohydrates",
            "Fat"
        ],
        "Value": [
            protein,
            carbs,
            fat
        ]
    }

    fig = px.pie(
        macro_data,
        names="Nutrient",
        values="Value",
        hole=0.4,
        title="Macronutrient Composition"
    )

    return fig


# --------------------------------------------------
# CORRELATION HEATMAP
# --------------------------------------------------

def correlation_heatmap(df):

    numeric_cols = [
        col for col in df.columns
        if df[col].dtype != "object"
    ]

    corr = df[numeric_cols].corr()

    fig = ff.create_annotated_heatmap(
        z=np.round(
            corr.values,
            2
        ),
        x=list(corr.columns),
        y=list(corr.columns),
        annotation_text=np.round(
            corr.values,
            2
        ),
        showscale=True
    )

    fig.update_layout(
        title="Correlation Heatmap",
        height=700
    )

    return fig


# --------------------------------------------------
# BMI VS PROTEIN
# --------------------------------------------------

def bmi_protein_chart(df):

    fig = px.scatter(
        df,
        x="Protein_Intake_g",
        y="BMI",
        color="Health_Status",
        title="Protein Intake vs BMI"
    )

    return fig


# --------------------------------------------------
# CALORIE BALANCE CHART
# --------------------------------------------------

def calorie_balance_chart(df):

    fig = px.histogram(
        df,
        x="Calorie_Balance",
        nbins=30,
        title="Calorie Balance Distribution"
    )

    return fig


# --------------------------------------------------
# RISK SCORE CHART
# --------------------------------------------------

def risk_score_chart(df):

    fig = px.histogram(
        df,
        x="Risk_Score",
        nbins=20,
        title="Health Risk Score Distribution"
    )

    return fig


# --------------------------------------------------
# RISK CATEGORY CHART
# --------------------------------------------------

def risk_category_chart(df):

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
        title="Risk Category Distribution"
    )

    return fig


# --------------------------------------------------
# AI CLUSTER CHART
# --------------------------------------------------

def cluster_chart(df):

    fig = px.scatter(
        df,
        x="BMI",
        y="Daily_Calorie_Consumed",
        color="Cluster",
        title="AI Population Segmentation"
    )

    return fig
