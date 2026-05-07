import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def main():
    st.set_page_config(page_title="AI Data Analyst", page_icon="", layout="wide")
    st.title(" AI Data Analyst for CSV Files")
    st.markdown("Upload a CSV file, explore its properties, and clean the data.")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            # Initialize session state for the dataframe if it doesn't exist to retain modifications
            if 'original_df' not in st.session_state or st.session_state.get('uploaded_filename') != uploaded_file.name:
                raw_df = pd.read_csv(uploaded_file)
                st.session_state['original_df'] = raw_df.copy()
                
                # Auto-clean data
                df = raw_df.drop_duplicates()
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
                
                st.session_state['df'] = df
                st.session_state['uploaded_filename'] = uploaded_file.name
                st.session_state['is_cleaned'] = True
            
            df = st.session_state['df']
            
            # --- 1. Data Overview ---
            st.header("1. Data Overview")
            
            st.subheader("Dataset Preview")
            st.dataframe(df.head())
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Rows", df.shape[0])
            col2.metric("Columns", df.shape[1])
            col3.metric("Missing Values", df.isna().sum().sum())
            col4.metric("Duplicates", df.duplicated().sum())
            
            row1_col1, row1_col2 = st.columns(2)
            
            with row1_col1:
                st.subheader("Column Information")
                col_info = pd.DataFrame({
                    "Column": df.columns,
                    "Data Type": df.dtypes.astype(str),
                    "Missing Values": df.isnull().sum(),
                    "Missing %": (df.isnull().sum() / len(df) * 100).round(2)
                }).reset_index(drop=True)
                st.dataframe(col_info, use_container_width=True)
            
            with row1_col2:
                st.subheader("Missing Values Heatmap")
                if df.isna().sum().sum() > 0:
                    fig, ax = plt.subplots(figsize=(6, 4))
                    sns.heatmap(df.isnull(), yticklabels=False, cbar=False, cmap='viridis', ax=ax)
                    plt.tight_layout()
                    st.pyplot(fig)
                else:
                    st.success("No missing values found!")

            # --- 2. Data Cleaning & Export ---
            st.header("2. Data Cleaning & Export")
            
            if st.session_state.get('is_cleaned', True):
                st.success("Data was automatically cleaned upon upload! (Duplicates dropped, missing numeric values filled with median)")
                
                # Download button for cleaned data
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download Cleaned Data as CSV",
                    data=csv,
                    file_name='cleaned_data.csv',
                    mime='text/csv',
                    type="primary"
                )

                if st.button("Revert to Original Uncleaned Data"):
                    st.session_state['df'] = st.session_state['original_df'].copy()
                    st.session_state['is_cleaned'] = False
                    st.rerun()
            else:
                st.warning("Currently viewing original uncleaned data.")
                if st.button("Clean Data Again", type="primary"):
                    df = st.session_state['df']
                    df = df.drop_duplicates()
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
                    st.session_state['df'] = df
                    st.session_state['is_cleaned'] = True
                    st.rerun()

            # --- 3. Statistical Summary & Correlation ---
            st.header("3. Statistical Summary & Correlation")
            
            st.subheader("Statistical Summary (Numeric)")
            st.dataframe(df.describe())
            
            st.subheader("Correlation Matrix")
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty and numeric_df.shape[1] > 1:
                fig, ax = plt.subplots(figsize=(10, 8))
                corr_matrix = numeric_df.corr()
                sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info("Not enough numeric columns to generate a correlation matrix.")
                
            # --- 4. Data Visualization ---
            st.header("4. Data Visualization")
            
            plot_type = st.selectbox("Choose a plot type", ["Scatter Plot", "Bar Chart", "Histogram", "Box Plot"])
            
            if plot_type == "Scatter Plot":
                x_axis = st.selectbox("Select X-axis", df.columns, key='scatter_x')
                y_axis = st.selectbox("Select Y-axis", df.columns, key='scatter_y')
                if st.button("Generate Scatter Plot"):
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
                    st.pyplot(fig)
                    
            elif plot_type == "Bar Chart":
                x_axis = st.selectbox("Select X-axis (Categorical/Discrete)", df.columns, key='bar_x')
                y_axis = st.selectbox("Select Y-axis (Numeric)", df.select_dtypes(include=[np.number]).columns, key='bar_y')
                if st.button("Generate Bar Chart"):
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.barplot(data=df, x=x_axis, y=y_axis, ax=ax)
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    
            elif plot_type == "Histogram":
                x_axis = st.selectbox("Select Column (Numeric)", df.select_dtypes(include=[np.number]).columns, key='hist_x')
                bins = st.slider("Number of bins", min_value=5, max_value=100, value=20)
                if st.button("Generate Histogram"):
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.histplot(data=df, x=x_axis, bins=bins, kde=True, ax=ax)
                    st.pyplot(fig)
                    
            elif plot_type == "Box Plot":
                x_axis = st.selectbox("Select Categorical Column (Optional X-axis)", ['None'] + list(df.columns), key='box_x')
                y_axis = st.selectbox("Select Numeric Column (Y-axis)", df.select_dtypes(include=[np.number]).columns, key='box_y')
                if st.button("Generate Box Plot"):
                    fig, ax = plt.subplots(figsize=(8, 6))
                    if x_axis == 'None':
                        sns.boxplot(data=df, y=y_axis, ax=ax)
                    else:
                        sns.boxplot(data=df, x=x_axis, y=y_axis, ax=ax)
                        plt.xticks(rotation=45)
                    st.pyplot(fig)




        except Exception as e:
            st.error(f"An error occurred while processing the file: {str(e)}")

if __name__ == "__main__":
    main()
