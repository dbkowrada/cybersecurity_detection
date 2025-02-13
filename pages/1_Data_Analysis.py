# pages/1_Data_Analysis.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
from utils.preprocessing import get_feature_descriptions

# Page config
st.set_page_config(page_title="Data Analysis", page_icon="📊", layout="wide")

# Title
st.title("📊 Data Analysis & Visualization")
st.markdown("Analyze and understand your cybersecurity data patterns")

def display_dtypes_table(df):
    """Display DataFrame dtypes in a more streamlit-friendly way."""
    dtype_dict = {'Column': [], 'Type': [], 'Non-Null Count': [], 'Null Count': []}
    for column in df.columns:
        dtype_dict['Column'].append(column)
        dtype_dict['Type'].append(str(df[column].dtype))
        dtype_dict['Non-Null Count'].append(df[column].count())
        dtype_dict['Null Count'].append(df[column].isnull().sum())
    
    return pd.DataFrame(dtype_dict)

# File upload
uploaded_file = st.file_uploader(
    "Upload your cybersecurity data (CSV)",
    type=['csv'],
    help="Upload a CSV file containing cybersecurity attack data"
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Dataset Loaded Successfully!")
        
        # Create tabs for different analyses
        tabs = st.tabs([
            "📋 Overview",
            "❓ Missing Values",
            "📊 Distribution Analysis",
            "🔗 Correlation Analysis",
            "🔍 Feature Analysis"
        ])
        
        # Overview Tab
        with tabs[0]:
            st.header("Dataset Overview")
            
            # Basic statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Features", len(df.columns))
            with col3:
                st.metric("Attack Types", len(df['Attack Type'].unique()) if 'Attack Type' in df.columns else "N/A")
            
            # Dataset info
            st.subheader("Dataset Information")
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())
            
            # Sample data
            st.subheader("Sample Data")
            st.dataframe(df.head())
            
            # Data types summary
            st.subheader("Data Types Summary")
            dtype_df = display_dtypes_table(df)
            st.dataframe(dtype_df)
        
        # Missing Values Tab
        with tabs[1]:
            st.header("Missing Values Analysis")
            
            # Missing values summary
            missing = pd.DataFrame({
                'Column': df.columns,
                'Missing Values': df.isnull().sum(),
                'Percentage': (df.isnull().sum() / len(df) * 100).round(2)
            }).sort_values('Missing Values', ascending=False)
            
            st.dataframe(missing)
            
            # Missing values heatmap
            if missing['Missing Values'].sum() > 0:
                st.subheader("Missing Values Heatmap")
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.heatmap(df.isnull(), yticklabels=False, cbar=False, cmap='viridis')
                st.pyplot(fig)
            else:
                st.success("No missing values found in the dataset!")
        
        # Distribution Analysis Tab
        with tabs[2]:
            st.header("Distribution Analysis")
            
            if 'Attack Type' in df.columns:
                # Attack type distribution
                st.subheader("Attack Type Distribution")
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.countplot(data=df, x='Attack Type')
                plt.xticks(rotation=45)
                st.pyplot(fig)
                
                # Percentage distribution
                st.subheader("Attack Type Percentages")
                attack_dist = df['Attack Type'].value_counts(normalize=True) * 100
                percentage_df = pd.DataFrame({
                    'Attack Type': attack_dist.index,
                    'Percentage': attack_dist.values.round(2)
                })
                st.dataframe(percentage_df)
            
            # Numerical features distribution
            st.subheader("Numerical Features Distribution")
            num_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(num_cols) > 0:
                selected_feature = st.selectbox("Select Feature", num_cols)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Histogram
                    fig, ax = plt.subplots()
                    sns.histplot(data=df, x=selected_feature, kde=True)
                    plt.title(f"Distribution of {selected_feature}")
                    st.pyplot(fig)
                
                with col2:
                    # Box plot
                    fig, ax = plt.subplots()
                    sns.boxplot(data=df, y=selected_feature)
                    plt.title(f"Box Plot of {selected_feature}")
                    st.pyplot(fig)
                
                # Statistics
                st.subheader(f"Statistics for {selected_feature}")
                stats_df = pd.DataFrame({
                    'Statistic': ['Mean', 'Median', 'Std Dev', 'Min', 'Max'],
                    'Value': [
                        df[selected_feature].mean(),
                        df[selected_feature].median(),
                        df[selected_feature].std(),
                        df[selected_feature].min(),
                        df[selected_feature].max()
                    ]
                })
                st.dataframe(stats_df)
        
        # Correlation Analysis Tab
        with tabs[3]:
            st.header("Feature Correlations")
            
            numerical_cols = df.select_dtypes(include=[np.number]).columns
            if len(numerical_cols) > 0:
                # Correlation matrix
                corr_matrix = df[numerical_cols].corr()
                
                # Heatmap
                st.subheader("Correlation Heatmap")
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
                st.pyplot(fig)
                
                # Detailed correlations
                st.subheader("Detailed Correlation Analysis")
                st.dataframe(corr_matrix.style.background_gradient(cmap="coolwarm"))
        
        # Feature Analysis Tab
        with tabs[4]:
            st.header("Feature Analysis")
            
            # Get feature descriptions
            feature_desc = get_feature_descriptions()
            
            # Feature selection
            selected_feature = st.selectbox("Select Feature for Analysis", df.columns)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Description**: {feature_desc.get(selected_feature, 'No description available')}")
                st.markdown(f"**Data Type**: {df[selected_feature].dtype}")
                st.markdown(f"**Unique Values**: {df[selected_feature].nunique()}")
                
                if df[selected_feature].dtype in ['int64', 'float64']:
                    st.markdown(f"**Mean**: {df[selected_feature].mean():.2f}")
                    st.markdown(f"**Std Dev**: {df[selected_feature].std():.2f}")
                    st.markdown(f"**Range**: {df[selected_feature].min():.2f} - {df[selected_feature].max():.2f}")
            
            with col2:
                if df[selected_feature].dtype in ['int64', 'float64']:
                    fig, ax = plt.subplots()
                    sns.histplot(data=df, x=selected_feature, kde=True)
                    plt.title(f"Distribution of {selected_feature}")
                    st.pyplot(fig)
                else:
                    st.subheader("Value Counts")
                    st.dataframe(df[selected_feature].value_counts().head())
    
    except Exception as e:
        st.error(f"Error analyzing data: {str(e)}")
else:
    st.info("Please upload a CSV file to begin analysis")

# Sidebar information
st.sidebar.header("📋 Analysis Guide")
st.sidebar.markdown("""
### Analysis Steps
1. Start with the Overview to understand your data
2. Check Missing Values to identify data quality issues
3. Use Distribution Analysis to understand patterns
4. Examine Correlations to find relationships
5. Review Feature Analysis for detailed insights
""")

# Session state status
if 'model' in st.session_state and st.session_state['model'] is not None:
    st.sidebar.success("Model is trained and ready")
else:
    st.sidebar.warning("No model trained yet")