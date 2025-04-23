from io import BytesIO

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="CSV Analyzer", layout="wide")
st.markdown(
    "<h1 style='text-align: center;'>📊 CSV Analyzer</h1>", unsafe_allow_html=True
)
st.divider()

# Session State Initialization
if "data" not in st.session_state:
    st.session_state.data = None

# File Upload
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])
st.divider()

# Store file in session state
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.session_state.data = df

# Use stored data
df = st.session_state.data

if df is not None:
    page = st.sidebar.radio(
        "📌 Navigate",
        [
            "Home",
            "Summary Statistics",
            "Missing Values",
            "Visualizations",
            "Data Filter",
            "Download Report",
        ],
    )

    if page == "Home":
        st.subheader("👁️ Data Preview")
        st.dataframe(df.head())

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🔢 Numerical Columns")
            st.dataframe(df.select_dtypes(include=[np.number]).head())
        with col2:
            st.markdown("#### 🔤 Categorical Columns")
            st.dataframe(df.select_dtypes(exclude=[np.number]).head())

    elif page == "Summary Statistics":
        st.subheader("📈 Summary Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🔢 Numerical")
            st.dataframe(df.describe(include=[np.number]))
        with col2:
            st.markdown("#### 🔤 Categorical")
            st.dataframe(df.describe(include=["object"]))

        st.markdown("#### 📋 Column Data Types")
        st.dataframe(df.dtypes)

    elif page == "Missing Values":
        st.subheader("❗ Missing Values")
        missing = df.isnull().sum()
        st.dataframe(
            missing[missing > 0] if missing.any() else "✅ No missing values found!"
        )

    elif page == "Visualizations":
        st.subheader("📊 Data Visualizations")
        tab1, tab2, tab3 = st.tabs(["Overview", "Histograms", "Categorical Charts"])

        with tab1:
            column = st.selectbox(
                "Select a column to visualize:", df.columns, key="col_overview"
            )
            if pd.api.types.is_numeric_dtype(df[column]):
                st.bar_chart(df[column])
            else:
                st.write(df[column].value_counts())
                st.bar_chart(df[column].value_counts())

        with tab2:
            num_cols = df.select_dtypes(include="number").columns
            if num_cols.any():
                hist_col = st.selectbox(
                    "📌 Choose numeric column:", num_cols, key="hist_col"
                )
                fig = px.histogram(
                    df, x=hist_col, nbins=20, title=f"Distribution of {hist_col}"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No numeric columns available for histogram.")

        with tab3:
            cat_cols = df.select_dtypes(exclude="number").columns
            if cat_cols.any():
                cat_col = st.selectbox(
                    "📌 Choose categorical column:", cat_cols, key="cat_col"
                )
                freq = df[cat_col].value_counts().reset_index()
                freq.columns = [cat_col, "Count"]
                fig = px.bar(
                    freq,
                    x=cat_col,
                    y="Count",
                    color="Count",
                    title=f"Frequency of {cat_col}",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No categorical columns available for bar chart.")

    elif page == "Data Filter":
        st.subheader("🔍 Filter Your Data")
        filter_col = st.selectbox("Select a column to filter:", df.columns)
        unique_vals = df[filter_col].dropna().unique()
        selected_val = st.selectbox(f"Select value for {filter_col}", unique_vals)
        filtered_df = df[df[filter_col] == selected_val]
        st.write(filtered_df)

    elif page == "Download Report":
        st.subheader("📥 Download Filtered Data")
        output = BytesIO()
        df.to_csv(output, index=False)
        st.download_button(
            "Download CSV",
            data=output.getvalue(),
            file_name="cleaned_data.csv",
            mime="text/csv",
        )
