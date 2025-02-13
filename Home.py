# Home.py
import streamlit as st

st.set_page_config(
    page_title="Cybersecurity Attack Detection",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'model' not in st.session_state:
    st.session_state['model'] = None
if 'label_encoders' not in st.session_state:
    st.session_state['label_encoders'] = None
if 'feature_names' not in st.session_state:
    st.session_state['feature_names'] = None

# Main content
st.title("🔒 Cybersecurity Attack Detection System")

# Description with improved formatting
st.markdown("""
## Welcome to the Cybersecurity Attack Analysis Platform

This advanced system uses machine learning to detect and classify cybersecurity attacks, providing:

### 🎯 Core Capabilities

1. **Comprehensive Data Analysis**
   - Interactive data visualization
   - Pattern recognition
   - Statistical analysis
   - Missing value detection

2. **Advanced Model Training**
   - Multiple ML algorithms
   - Performance comparison
   - Feature importance analysis
   - Model evaluation metrics

3. **Flexible Prediction Options**
   - Real-time single predictions
   - Batch processing capability
   - Detailed result analysis
   - Export functionality
""")

# Quick start guide
st.header("🚀 Quick Start Guide")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### Step 1: Data Analysis
    - Go to **Data Analysis** page
    - Upload your CSV file
    - Explore data patterns
    - Analyze feature distributions
    """)

with col2:
    st.markdown("""
    ### Step 2: Model Training
    - Navigate to **Model Training**
    - Select your preferred model
    - Train and evaluate
    - Review performance metrics
    """)

with col3:
    st.markdown("""
    ### Step 3: Make Predictions
    - Choose **Single** or **Batch** prediction
    - Input required data
    - Get instant predictions
    - Export results
    """)

# System status
st.sidebar.header("System Status")
if st.session_state['model'] is None:
    st.sidebar.warning("No model trained yet")
else:
    st.sidebar.success("Model ready for predictions")

# Additional information
st.markdown("""
---
### 📊 Supported Data Format

Your input data should include these key features:
- Source/Destination IP Addresses
- Port numbers
- Protocol information
- Packet details
- Network metrics

### 🤖 Available Models

1. **Random Forest**
   - Balanced performance
   - Good for mixed data types

2. **XGBoost**
   - High accuracy
   - Excellent feature importance

3. **Gradient Boosting**
   - Strong pattern detection
   - Robust to outliers

4. **Neural Network**
   - Deep pattern recognition
   - Scalable to large datasets
""")

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit*")
