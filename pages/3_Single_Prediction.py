# pages/3_Single_Prediction.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils.preprocessing import preprocess_data
import json
from datetime import datetime

# Page config
st.set_page_config(page_title="Single Prediction", page_icon="🎯", layout="wide")

# Title
st.title("🎯 Single Attack Prediction")
st.markdown("Input network event details to predict the attack type")

# Check if model is trained
if 'model' not in st.session_state or st.session_state['model'] is None:
    st.error("⚠️ No trained model found. Please train a model first!")
    st.stop()

# Create input form
st.header("Enter Security Event Details")

# Create three columns for input fields
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Network Information")
    source_port = st.number_input(
        "Source Port",
        min_value=0,
        max_value=65535
    )
    
    dest_port = st.number_input(
        "Destination Port",
        min_value=0,
        max_value=65535
    )
    
    packet_length = st.number_input(
        "Packet Length",
        min_value=0
    )

with col2:
    st.subheader("Attack Indicators")
    anomaly_score = st.slider(
        "Anomaly Score",
        min_value=0.0,
        max_value=1.0,
        value=0.5
    )
    
    attack_signature = st.text_input("Attack Signature")

with col3:
    st.subheader("Additional Information")
    source_ip = st.text_input("Source IP")
    dest_ip = st.text_input("Destination IP")

# Make prediction button
if st.button("Predict Attack Type", type="primary"):
    try:
        # Create DataFrame from inputs
        input_data = pd.DataFrame({
            'Source Port': [source_port],
            'Destination Port': [dest_port],
            'Packet Length': [packet_length],
            'Anomaly Scores': [anomaly_score],
            'Attack Signature': [attack_signature],
            'Source IP Address': [source_ip],
            'Destination IP Address': [dest_ip]
        })
        
        # Preprocess input data
        processed_input, _ = preprocess_data(input_data, is_training=False)
        
        # Ensure all required features are present
        missing_cols = set(st.session_state['feature_names']) - set(processed_input.columns)
        for col in missing_cols:
            processed_input[col] = 0
            
        # Reorder columns to match training data
        processed_input = processed_input[st.session_state['feature_names']]
        
        # Make prediction
        prediction = st.session_state['model'].predict(processed_input)
        
        # Get prediction probability if available
        probabilities = None
        if hasattr(st.session_state['model'], 'predict_proba'):
            probabilities = st.session_state['model'].predict_proba(processed_input)
            max_prob = np.max(probabilities)
        
        # Convert prediction to actual attack type
        if 'attack_type_labels' in st.session_state:
            attack_type = st.session_state['attack_type_labels'].get(prediction[0], prediction[0])
        else:
            attack_type = prediction[0]
        
        # Display results
        st.header("Prediction Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"🎯 Predicted Attack Type: **{attack_type}**")
            if probabilities is not None:
                # Show all probabilities
                st.subheader("Confidence Scores for Each Attack Type")
                for i, prob in enumerate(probabilities[0]):
                    attack_label = st.session_state['attack_type_labels'].get(i, f"Type {i}")
                    st.metric(f"{attack_label}", f"{prob:.2%}")
                
                st.info("""
                Note: While the model achieves 100% accuracy on training data,
                confidence scores show how well new data matches known patterns.
                Lower confidence doesn't mean incorrect prediction, just less certainty.
                """)
        
        with col2:
            # Feature importance if available
            if hasattr(st.session_state['model'], 'feature_importances_'):
                importances = st.session_state['model'].feature_importances_
                importance_df = pd.DataFrame({
                    'Feature': st.session_state['feature_names'],
                    'Importance': importances
                }).sort_values('Importance', ascending=False)
                
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(data=importance_df.head(10), x='Importance', y='Feature')
                plt.title("Top 10 Most Important Features")
                st.pyplot(fig)
        
        # Save prediction to history
        if 'prediction_history' not in st.session_state:
            st.session_state['prediction_history'] = []
        
        prediction_record = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'input_values': input_data.to_dict('records')[0],
            'prediction': attack_type,
            'confidence': float(max_prob) if probabilities is not None else None
        }
        
        st.session_state['prediction_history'].append(prediction_record)
        
        # Display prediction history
        if st.session_state['prediction_history']:
            st.header("Prediction History")
            history_df = pd.DataFrame(st.session_state['prediction_history'])
            st.dataframe(history_df)
            
            # Download predictions
            if st.download_button(
                "Download Prediction History",
                data=json.dumps(st.session_state['prediction_history'], indent=2),
                file_name="prediction_history.json",
                mime="application/json"
            ):
                st.success("Prediction history downloaded successfully!")
                
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        import traceback
        st.error(traceback.format_exc())

# Sidebar information
st.sidebar.header("ℹ️ Input Guide")
st.sidebar.markdown("""
### Required Fields
- Source Port
- Destination Port
- Packet Length
- Anomaly Score
- Attack Signature

### Tips
1. Provide as much information as possible
2. Check prediction confidence
3. Review feature impacts
""")

# Display model status
st.sidebar.header("🤖 Model Status")
model_type = type(st.session_state['model']).__name__
st.sidebar.success(f"Using {model_type} model")