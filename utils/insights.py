import pandas as pd


# --------------------------------------------------
# BMI INSIGHTS
# --------------------------------------------------

def bmi_insights(df):

    insights = []

    avg_bmi = round(
        df["BMI"].mean(),
        2
    )

    if avg_bmi < 18.5:

        insights.append(
            f"Average BMI is {avg_bmi}. Population appears underweight."
        )

    elif avg_bmi < 25:

        insights.append(
            f"Average BMI is {avg_bmi}. Population is within a healthy range."
        )

    elif avg_bmi < 30:

        insights.append(
            f"Average BMI is {avg_bmi}. Population shows overweight tendencies."
        )

    else:

        insights.append(
            f"Average BMI is {avg_bmi}. Population is at obesity risk."
        )

    return insights


# --------------------------------------------------
# CALORIE INSIGHTS
# --------------------------------------------------

def calorie_insights(df):

    insights = []

    avg_consumed = (
        df["Daily_Calorie_Consumed"]
        .mean()
    )

    avg_required = (
        df["Daily_Calorie_Requirement"]
        .mean()
    )

    difference = (
        avg_consumed
        -
        avg_required
    )

    if difference > 200:

        insights.append(
            f"Average calorie surplus detected (+{difference:.0f} kcal)."
        )

    elif difference < -200:

        insights.append(
            f"Average calorie deficit detected ({difference:.0f} kcal)."
        )

    else:

        insights.append(
            "Calorie intake is close to recommended requirements."
        )

    return insights


# --------------------------------------------------
# PROTEIN INSIGHTS
# --------------------------------------------------

def protein_insights(df):

    insights = []

    if "Protein_Intake_g" not in df.columns:
        return insights

    avg_protein = round(
        df["Protein_Intake_g"].mean(),
        2
    )

    if avg_protein < 60:

        insights.append(
            f"Average protein intake is low ({avg_protein} g)."
        )

    elif avg_protein < 90:

        insights.append(
            f"Average protein intake is moderate ({avg_protein} g)."
        )

    else:

        insights.append(
            f"Average protein intake is high ({avg_protein} g)."
        )

    return insights


# --------------------------------------------------
# WATER INTAKE INSIGHTS
# --------------------------------------------------

def water_insights(df):

    insights = []

    if "Water_Intake_Liters" not in df.columns:
        return insights

    avg_water = round(
        df["Water_Intake_Liters"].mean(),
        2
    )

    if avg_water < 2:

        insights.append(
            f"Average water intake is low ({avg_water} L/day)."
        )

    else:

        insights.append(
            f"Average water intake is healthy ({avg_water} L/day)."
        )

    return insights


# --------------------------------------------------
# DIET TYPE INSIGHTS
# --------------------------------------------------

def diet_insights(df):

    insights = []

    if "Diet_Type" not in df.columns:
        return insights

    top_diet = (
        df["Diet_Type"]
        .value_counts()
        .idxmax()
    )

    diet_percentage = round(
        (
            df["Diet_Type"]
            .value_counts(normalize=True)
            .max()
        ) * 100,
        2
    )

    insights.append(
        f"Most common diet type is '{top_diet}' ({diet_percentage}% of population)."
    )

    return insights


# --------------------------------------------------
# HEALTH STATUS INSIGHTS
# --------------------------------------------------

def health_status_insights(df):

    insights = []

    if "Health_Status" not in df.columns:
        return insights

    top_status = (
        df["Health_Status"]
        .value_counts()
        .idxmax()
    )

    percentage = round(
        (
            df["Health_Status"]
            .value_counts(normalize=True)
            .max()
        ) * 100,
        2
    )

    insights.append(
        f"Most individuals belong to '{top_status}' category ({percentage}%)."
    )

    return insights


# --------------------------------------------------
# RISK INSIGHTS
# --------------------------------------------------

def risk_insights(df):

    insights = []

    if "Risk_Score" not in df.columns:
        return insights

    avg_risk = round(
        df["Risk_Score"].mean(),
        2
    )

    if avg_risk < 20:

        insights.append(
            f"Average risk score is {avg_risk}. Overall population risk is low."
        )

    elif avg_risk < 50:

        insights.append(
            f"Average risk score is {avg_risk}. Population has moderate health risks."
        )

    else:

        insights.append(
            f"Average risk score is {avg_risk}. High health risk population detected."
        )

    return insights


# --------------------------------------------------
# CLUSTER INSIGHTS
# --------------------------------------------------

def cluster_insights(df):

    insights = []

    if "Cluster" not in df.columns:
        return insights

    total_clusters = (
        df["Cluster"]
        .nunique()
    )

    insights.append(
        f"AI segmentation identified {total_clusters} unique population clusters."
    )

    return insights


# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------

def executive_summary(df):

    summary = []

    summary.extend(
        bmi_insights(df)
    )

    summary.extend(
        calorie_insights(df)
    )

    summary.extend(
        protein_insights(df)
    )

    summary.extend(
        water_insights(df)
    )

    summary.extend(
        diet_insights(df)
    )

    summary.extend(
        health_status_insights(df)
    )

    return summary


# --------------------------------------------------
# GENERATE ALL INSIGHTS
# --------------------------------------------------

def generate_all_insights(df):

    insights = []

    insights.extend(
        bmi_insights(df)
    )

    insights.extend(
        calorie_insights(df)
    )

    insights.extend(
        protein_insights(df)
    )

    insights.extend(
        water_insights(df)
    )

    insights.extend(
        diet_insights(df)
    )

    insights.extend(
        health_status_insights(df)
    )

    insights.extend(
        risk_insights(df)
    )

    insights.extend(
        cluster_insights(df)
    )

    return insights


# --------------------------------------------------
# STREAMLIT DISPLAY HELPER
# --------------------------------------------------

def display_insights(st, insights):

    for insight in insights:

        st.info(insight)
