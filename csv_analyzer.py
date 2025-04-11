# Step 1: Basic Setup

## Import Libraries
import streamlit as st
import pandas as pd
import seaborn as sns

## Set the title of the Website
st.title("📊 CSV Analyzer")

## Upload Data And Data Preview
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    ### Display the First five rows of the data
    st.subheader("🔍 Data Preview")
    st.write(df.head())
    ### Display the number of rows and columns of the data
    st.subheader("📐 Shape of Data")
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

# Step 2: Add Summary Statistics
    ### Summary statistics table
    st.subheader("📊 Summary Statistics")
    st.write(df.describe())

    ### view columns data type
    st.subheader("📂 Column Data Types")
    st.write(df.dtypes)

# Step 3: Handle Missing Values
    ### Check for Missing Values
    st.subheader("⚠️ Missing Values")
    st.write(df.isnull().sum())

    ### Drop Missing Values
    if st.checkbox("Drop rows with missing values"):
        df = df.dropna()
        st.success("Dropped missing values!")

# Step 4: Column Selector and Visualizations
    st.subheader("📈 Column-wise Visualization")

    column = st.selectbox("Choose a column to visualize", df.columns)

    if df[column].dtype in ['int64', 'float64']:
        st.bar_chart(df[column])
    else:
        st.write(df[column].value_counts().plot(kind="bar"))
        st.pyplot()
### Optional Use ```Seaborn.histplot()``` for better control of histogram visuals

# Step 5: Add Filters (Bonus)
    st.subheader("🔎 Filter Data by Column Value")

    selected_col = st.selectbox("Choose a column to filter", df.columns)

    if df[selected_col].dtype == 'object':
        options = df[selected_col].unique()
        selected_option = st.selectbox("Filter by", options)
        filtered_df = df[df[selected_col] == selected_option]
        st.write(filtered_df)
##################################################################################################################