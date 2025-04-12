import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from narwhals.selectors import categorical

st.markdown("<h1 style='text-align: center;'>CSV Analyzer</h1>", unsafe_allow_html=True)
st.divider()
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
st.divider()

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    sidebar = st.sidebar.selectbox("Choose from Below", ['Home', 'Summary Statistics', 'Missing Values', 'Visualizations'])
    if sidebar == 'Home':
        st.write("Data Preview")
        st.write(df.head())
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.write("Numerical Columns")
            st.write(df.select_dtypes(include=[np.number]).head())
            st.divider()
        with col2:
            st.write("Categorical Columns")
            st.write(df.select_dtypes(exclude=[np.number]).head())
            st.divider()

    elif sidebar == 'Summary Statistics':
        st.write("Summary Stats for Numerical Columns")
        st.write(df.describe(include = np.number))
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.write("Summary Stats for Categorical Columns")
            st.write(df.describe(include = 'object'))
            st.divider()
        with col2:
            st.write("Basic Information")
            st.write(df.dtypes)
            st.divider()

    elif sidebar == 'Missing Values':
        st.write("Missing Values")
        st.write(df.isnull().sum())
        st.divider()

    elif sidebar == 'Visualizations':
        st.subheader("Column-wise Visualization")
        tab1, tab2, tab3 = st.tabs(["Basic", "Histograms", "Bar Graphs"])
        with tab1:
            column = st.selectbox("Choose a column to visualize", df.columns)
            if df[column].dtype in ['int64', 'float64']:
                st.bar_chart(df[column])

            else:
                st.write(df[column].value_counts().plot(kind="bar"))
                st.pyplot()

        with tab2:
            numeric_cols = df.select_dtypes(include='number').columns.tolist()
            selected_col = st.selectbox("Pick a numeric column for histogram", numeric_cols)

            if selected_col:
                fig3 = px.histogram(df, x=selected_col, nbins=10, title=f'Distribution of {selected_col}')
                st.plotly_chart(fig3, use_container_width=True)

        with tab3:
            categorical_cols = df.select_dtypes(exclude='number').columns.tolist()
            selected_col = st.selectbox("Pick a numeric column for histogram", categorical_cols)
            if selected_col:
                freq_table = df[selected_col].value_counts().reset_index()
                fig = px.bar(df, x= freq_table.iloc[:, 1], y=freq_table.iloc[:, 1], orientation='h',
                             labels={'x': 'Frequency', 'y': ''}, title=f" Bar-Chart for {selected_col}", color = freq_table.iloc[:, 1])

                # Show in Streamlit
                st.plotly_chart(fig, use_container_width=True)
########################################################################################################################
