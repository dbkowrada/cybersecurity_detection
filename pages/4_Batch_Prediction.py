# pages/4_Batch_Prediction.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils.preprocessing import preprocess_data
from datetime import datetime

# Page config
st.set_page_config(page_title="Batch Prediction", page_icon="📊", layout="wide")

# Title
st.title("📊 Batch Attack Prediction")
st.markdown("Upload multiple records for batch prediction")

# Check if model is trained
if 'model' not in st.session_state or st.session_state['model'] is None:
    st.error("⚠️ No trained model found. Please train a model first!")
    st.stop()

# Provide sample template
st.header("1. Download Template")
st.markdown("Use this template as a reference for your input file format.")

sample_data = pd.DataFrame({
    'Source Port': [80, 443],
    'Destination Port': [8080, 22],
    'Packet Length': [1024, 2048],
    'Anomaly Scores': [0.7, 0.3],
    'Attack Signature': ['signature1', 'signature2'],
    'Source IP Address': ['192.168.1.1', '10.0.0.1'],
    'Destination IP Address': ['192.168.1.2', '10.0.0.2']
})

st.download_button(
    label="📥 Download Template CSV",
    data=sample_data.to_csv(index=False),
    file_name="template.csv",
    mime="text/csv"
)

# File upload section
st.header("2. Upload Your Data")
uploaded_file = st.file_uploader(
    "Upload your CSV file containing multiple records",
    type=['csv']
)

if uploaded_file is not None:
    try:
        # Load data
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Successfully loaded {len(df)} records")
        
        # Show data preview
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        # Generate predictions
        if st.button("Generate Predictions", type="primary"):
            with st.spinner("Processing... Please wait."):
                try:
                    # Preprocess data
                    processed_data, _ = preprocess_data(df, is_training=False)
                    
                    # Ensure all required features are present
                    missing_cols = set(st.session_state['feature_names']) - set(processed_data.columns)
                    for col in missing_cols:
                        processed_data[col] = 0
                    
                    # Reorder columns to match training data
                    processed_data = processed_data[st.session_state['feature_names']]
                    
                    # Make predictions
                    predictions = st.session_state['model'].predict(processed_data)
                    
                    # Get prediction probabilities if available
                    probabilities = None
                    confidence_scores = None
                    if hasattr(st.session_state['model'], 'predict_proba'):
                        probabilities = st.session_state['model'].predict_proba(processed_data)
                        confidence_scores = np.max(probabilities, axis=1)
                    
                    # Convert predictions to actual attack types
                    if 'attack_type_labels' in st.session_state:
                        predicted_labels = [st.session_state['attack_type_labels'].get(pred, pred) 
                                         for pred in predictions]
                    else:
                        predicted_labels = predictions
                    
                    # Create detailed prediction results
                    results = df.copy()
                    results['Predicted_Attack_Type'] = predicted_labels
                    
                    # Add confidence scores for each attack type
                    if probabilities is not None:
                        # Add overall confidence
                        results['Overall_Confidence'] = confidence_scores
                        
                        # Add individual confidences for each attack type
                        for i, attack_type in st.session_state['attack_type_labels'].items():
                            results[f'Confidence_{attack_type}'] = probabilities[:, i]
                    
                    # Display Results
                    st.header("3. Prediction Results")
                    
                    # Summary metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Records", len(predictions))
                    with col2:
                        st.metric("Unique Attack Types", len(set(predicted_labels)))
                    with col3:
                        if confidence_scores is not None:
                            avg_confidence = np.mean(confidence_scores) * 100
                            st.metric("Average Confidence", f"{avg_confidence:.2f}%")
                    
                    # Show confidence distribution
                    if confidence_scores is not None:
                        st.subheader("Confidence Distribution")
                        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
                        
                        # Histogram of confidence scores
                        sns.histplot(confidence_scores, ax=ax1)
                        ax1.set_title("Distribution of Confidence Scores")
                        ax1.set_xlabel("Confidence")
                        ax1.set_ylabel("Count")
                        
                        # Box plot of confidence by attack type
                        confidence_by_type = pd.DataFrame({
                            'Attack Type': predicted_labels,
                            'Confidence': confidence_scores
                        })
                        sns.boxplot(data=confidence_by_type, x='Attack Type', y='Confidence', ax=ax2)
                        ax2.set_title("Confidence by Attack Type")
                        ax2.tick_params(axis='x', rotation=45)
                        
                        st.pyplot(fig)
                    
                    # Prediction distribution
                    st.subheader("Attack Type Distribution")
                    fig, ax = plt.subplots(figsize=(10, 6))
                    pred_counts = pd.Series(predicted_labels).value_counts()
                    sns.barplot(x=pred_counts.index, y=pred_counts.values)
                    plt.xticks(rotation=45)
                    plt.title("Distribution of Predicted Attack Types")
                    st.pyplot(fig)
                    
                    # Detailed statistics
                    st.subheader("Prediction Statistics")
                    stats_df = pd.DataFrame({
                        'Attack Type': pred_counts.index,
                        'Count': pred_counts.values,
                        'Percentage': (pred_counts.values / len(predictions) * 100).round(2)
                    })
                    if confidence_scores is not None:
                        confidence_by_type = pd.DataFrame({
                            'Attack Type': predicted_labels,
                            'Confidence': confidence_scores
                        }).groupby('Attack Type')['Confidence'].agg(['mean', 'min', 'max']).round(3)
                        stats_df = stats_df.merge(confidence_by_type, left_on='Attack Type', right_index=True)
                        stats_df.rename(columns={
                            'mean': 'Avg Confidence',
                            'min': 'Min Confidence',
                            'max': 'Max Confidence'
                        }, inplace=True)
                    st.dataframe(stats_df)
                    
                    # Add explanation
                    st.info("""
                    Note about Confidence Scores:
                    - 100% Training Accuracy means the model makes correct final decisions
                    - Confidence scores show how similar new data is to training patterns
                    - Lower confidence doesn't necessarily mean incorrect prediction
                    - High variation in confidence might indicate unusual patterns
                    """)
                    
                    # Detailed results table
                    st.subheader("Detailed Results")
                    st.dataframe(results)
                    
                    # Download options
                    st.header("4. Download Results")
                    
                    # Prepare download data with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"batch_predictions_{timestamp}.csv"
                    
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=results.to_csv(index=False),
                        file_name=filename,
                        mime="text/csv",
                        help="Download the predictions with original data"
                    )
                    
                    # Save batch prediction history
                    if 'batch_prediction_history' not in st.session_state:
                        st.session_state['batch_prediction_history'] = []
                    
                    batch_record = {
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'records_processed': len(df),
                        'unique_predictions': len(set(predicted_labels)),
                        'file_name': uploaded_file.name
                    }
                    
                    st.session_state['batch_prediction_history'].append(batch_record)
                    
                    # Show batch history
                    if st.session_state['batch_prediction_history']:
                        st.header("Processing History")
                        history_df = pd.DataFrame(st.session_state['batch_prediction_history'])
                        st.dataframe(history_df)
                    
                except Exception as e:
                    st.error(f"Error during prediction: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())
                
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        st.info("Please ensure your CSV file is properly formatted")
else:
    st.info("Please upload a CSV file to begin batch prediction")

# Sidebar information
st.sidebar.header("📋 Usage Guide")
st.sidebar.markdown("""
### Steps to Follow:
1. Download the template CSV
2. Prepare your data using the template format
3. Upload your CSV file
4. Click 'Generate Predictions'
5. Review the results
6. Download the predictions

### Required Columns:
- Source Port
- Destination Port
- Packet Length
- Anomaly Scores
- Attack Signature
""")

# Model information
st.sidebar.header("🤖 Model Status")
if 'model' in st.session_state and st.session_state['model'] is not None:
    model_type = type(st.session_state['model']).__name__
    st.sidebar.success(f"Using {model_type} model")
    if 'attack_type_labels' in st.session_state:
        st.sidebar.write("Available Attack Types:")
        for code, label in st.session_state['attack_type_labels'].items():
            st.sidebar.write(f"- {label}")
else:
    st.sidebar.warning("No model loaded")