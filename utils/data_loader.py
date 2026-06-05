import pandas as pd
import streamlit as st


@st.cache_data
def load_data():

    df = pd.read_csv(
        "healthy_diet_calorie_intake.csv"
    )

    return df


@st.cache_data
def clean_data(df):

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove rows with all null values
    df = df.dropna(how="all")

    return df


def add_bmi_category(df):

    def classify_bmi(bmi):

        if bmi < 18.5:
            return "Underweight"

        elif bmi < 25:
            return "Normal"

        elif bmi < 30:
            return "Overweight"

        else:
            return "Obese"

    df["BMI_Category"] = df["BMI"].apply(
        classify_bmi
    )

    return df


def add_calorie_balance(df):

    df["Calorie_Balance"] = (
        df["Daily_Calorie_Consumed"]
        -
        df["Daily_Calorie_Requirement"]
    )

    return df


def add_risk_score(df):

    def calculate_risk(row):

        score = 0

        # BMI Risk
        if row["BMI"] >= 30:
            score += 40

        elif row["BMI"] >= 25:
            score += 20

        # Calorie Risk
        calorie_gap = abs(
            row["Daily_Calorie_Consumed"]
            -
            row["Daily_Calorie_Requirement"]
        )

        if calorie_gap > 500:
            score += 30

        elif calorie_gap > 250:
            score += 15

        # Water Intake Risk
        if (
            "Water_Intake_Liters"
            in row.index
        ):

            if row["Water_Intake_Liters"] < 2:
                score += 10

        return score

    df["Risk_Score"] = df.apply(
        calculate_risk,
        axis=1
    )

    return df


def add_risk_category(df):

    def category(score):

        if score < 20:
            return "Low Risk"

        elif score < 50:
            return "Medium Risk"

        else:
            return "High Risk"

    df["Risk_Category"] = (
        df["Risk_Score"]
        .apply(category)
    )

    return df


@st.cache_data
def preprocess_data():

    df = load_data()

    df = clean_data(df)

    df = add_bmi_category(df)

    df = add_calorie_balance(df)

    df = add_risk_score(df)

    df = add_risk_category(df)

    return df


def get_summary_metrics(df):

    metrics = {
        "Total Records":
            len(df),

        "Average BMI":
            round(
                df["BMI"].mean(),
                2
            ),

        "Average Calories Consumed":
            round(
                df[
                    "Daily_Calorie_Consumed"
                ].mean(),
                2
            ),

        "Average Calories Required":
            round(
                df[
                    "Daily_Calorie_Requirement"
                ].mean(),
                2
            )
    }

    return metrics


def get_top_diet(df):

    if "Diet_Type" in df.columns:

        return (
            df["Diet_Type"]
            .value_counts()
            .idxmax()
        )

    return None


def get_top_health_status(df):

    if "Health_Status" in df.columns:

        return (
            df["Health_Status"]
            .value_counts()
            .idxmax()
        )

    return None
