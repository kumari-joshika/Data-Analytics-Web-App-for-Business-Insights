# =========================
# IMPORTS
# =========================
import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Automated Analytics System",
    layout="wide",
    page_icon="📊"
)

st.markdown("""
<style>
.stApp {
    background-color: #f4f6fb;
}
h1, h2, h3 {
    color: #1f2a44;
}
[data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 AI Automated Analytics Web System")
st.write("A professional system to analyze real-world raw datasets")

# =========================
# DATABASE FUNCTIONS
# =========================
def get_connection():
    return sqlite3.connect("analytics.db", check_same_thread=False)

def save_dataframe_to_db(df):
    conn = get_connection()
    df.to_sql("uploaded_data", conn, if_exists="replace", index=False)
    conn.close()

def run_sql_query(query):
    conn = get_connection()
    result = pd.read_sql(query, conn)
    conn.close()
    return result

# =========================
# FORECAST FUNCTION
# =========================
def forecast_values(df, column, periods):
    data = df[[column]].dropna().reset_index(drop=True)
    data["time"] = np.arange(len(data))

    X = data[["time"]]
    y = data[column]

    model = LinearRegression()
    model.fit(X, y)

    future_time = np.arange(len(data), len(data) + periods).reshape(-1, 1)
    predictions = model.predict(future_time)

    return predictions

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # =========================
    # DATA QUALITY & CLEANING
    # =========================
    st.subheader("🧹 Data Quality Report")

    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]

    if not missing_cols.empty:
        st.warning("Missing values detected")
        st.dataframe(missing_cols)
    else:
        st.success("No missing values detected")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    df[categorical_cols] = df[categorical_cols].fillna("Unknown")

    st.success("Automatic data cleaning applied")

    save_dataframe_to_db(df)

    # =========================
    # TABS
    # =========================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Preview",
        "🗄 SQL",
        "📈 Charts",
        "🔮 Forecast",
        "📊 Insights"
    ])

    # -------------------------
    # PREVIEW
    # -------------------------
    with tab1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head())
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Numeric Columns", len(numeric_cols))

    # -------------------------
    # SQL
    # -------------------------
    with tab2:
        st.subheader("Run SQL Query")
        st.write("Table name: **uploaded_data**")
        query = st.text_area("SQL Query", "SELECT * FROM uploaded_data LIMIT 5")
        if st.button("Run Query"):
            try:
                result = run_sql_query(query)
                st.dataframe(result)
            except Exception as e:
                st.error(e)

    # -------------------------
    # CHARTS
    # -------------------------
    with tab3:
        st.subheader("Interactive Charts")

        if numeric_cols.any():
            y_col = st.selectbox("Numeric Column", numeric_cols)
            fig = px.line(df, y=y_col, title=f"{y_col} Trend", markers=True)
            st.plotly_chart(fig, use_container_width=True)

        if categorical_cols.any() and numeric_cols.any():
            x_col = st.selectbox("Category Column", categorical_cols)
            y_col2 = st.selectbox("Value Column", numeric_cols, key="bar")
            grouped = df.groupby(x_col)[y_col2].sum().reset_index()
            fig2 = px.bar(grouped, x=x_col, y=y_col2, title=f"{y_col2} by {x_col}")
            st.plotly_chart(fig2, use_container_width=True)

    # -------------------------
    # FORECAST
    # -------------------------
    with tab4:
        st.subheader("AI Forecasting")

        if numeric_cols.any():
            target = st.selectbox("Select column", numeric_cols)
            periods = st.slider("Future periods", 1, 12, 5)
            if st.button("Generate Forecast"):
                preds = forecast_values(df, target, periods)
                forecast_df = pd.DataFrame({
                    "Future Period": range(1, periods + 1),
                    "Predicted Value": preds
                })
                st.dataframe(forecast_df)

    # -------------------------
    # INSIGHTS
    # -------------------------
    with tab5:
        st.subheader("Automated Business Insights")

        for col in numeric_cols:
            st.markdown(f"### {col}")
            st.write("Mean:", round(df[col].mean(), 2))
            st.write("Median:", round(df[col].median(), 2))
            st.write("Max:", df[col].max())
            st.write("Min:", df[col].min())

            trend = df[col].iloc[-1] - df[col].iloc[0]
            if trend > 0:
                st.success("Overall trend is increasing 📈")
            elif trend < 0:
                st.warning("Overall trend is decreasing 📉")
            else:
                st.info("Trend is stable")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Cleaned Data", csv, "cleaned_data.csv")

else:
    st.info("⬆ Upload a dataset to start")
