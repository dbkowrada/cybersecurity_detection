# pages/2_Model_Training.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from utils.preprocessing import preprocess_data
import joblib

# Page config
st.set_page_config(page_title="Model Training", page_icon="🤖", layout="wide")

# Title
st.title("🤖 Model Training & Evaluation")
st.markdown("Train and evaluate different machine learning models for attack detection")

# File upload section
uploaded_file = st.file_uploader("Upload your training data (CSV)", type=['csv'])

if uploaded_file is not None:
    try:
        # Load data
        df = pd.read_csv(uploaded_file)
        st.success("✅ Dataset loaded successfully!")
        
        # Display basic dataset info
        st.header("Dataset Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Features", len(df.columns))
        with col3:
            st.metric("Attack Types", len(df['Attack Type'].unique()))
        
        # Save original Attack Type column
        attack_type = df['Attack Type'].copy()
        
        # First, encode Attack Type separately
        le = LabelEncoder()
        encoded_attack_type = le.fit_transform(attack_type.astype(str))
        
        # Store attack type mapping
        st.session_state['attack_type_labels'] = dict(zip(range(len(le.classes_)), le.classes_))
        st.session_state['attack_type_encoder'] = le
        st.success(f"Encoded {len(le.classes_)} attack types")
        
        # Remove Attack Type before preprocessing
        df_without_target = df.drop('Attack Type', axis=1)
        
        # Preprocess features
        df_processed, label_encoders, scaler = preprocess_data(df_without_target, is_training=True)
        
        # Store preprocessing objects in session state
        st.session_state['label_encoders'] = label_encoders
        st.session_state['scaler'] = scaler
        st.session_state['feature_names'] = list(df_processed.columns)
        
        # Prepare data for modeling
        X = df_processed
        y = encoded_attack_type
        
        # Model Configuration
        st.header("Model Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            model_option = st.selectbox(
                "Select Model",
                ["Random Forest", "XGBoost", "Gradient Boosting", "Neural Network"]
            )
        
        with col2:
            # Model specific parameters
            if model_option in ["Random Forest", "XGBoost", "Gradient Boosting"]:
                n_estimators = st.slider("Number of trees", 100, 1000, 900)
            elif model_option == "Neural Network":
                epochs = st.slider("Number of epochs", 10, 100, 30)
        
        # Training button
        if st.button("Train Model", type="primary"):
            with st.spinner("Training model... Please wait."):
                try:
                    # Train selected model
                    if model_option == "Random Forest":
                        model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
                        model.fit(X, y)
                        y_pred = model.predict(X)
                        
                    elif model_option == "XGBoost":
                        model = XGBClassifier(n_estimators=n_estimators, random_state=42)
                        model.fit(X, y)
                        y_pred = model.predict(X)
                        
                    elif model_option == "Gradient Boosting":
                        model = GradientBoostingClassifier(n_estimators=n_estimators, random_state=42)
                        model.fit(X, y)
                        y_pred = model.predict(X)
                        
                    else:  # Neural Network
                        num_classes = len(np.unique(y))
                        model = Sequential([
                            Dense(128, input_dim=X.shape[1], activation='relu'),
                            Dense(64, activation='relu'),
                            Dense(32, activation='relu'),
                            Dense(num_classes, activation='softmax')
                        ])
                        model.compile(optimizer='adam', 
                                    loss='sparse_categorical_crossentropy',
                                    metrics=['accuracy'])
                        
                        model.fit(X, y, epochs=epochs, batch_size=32, verbose=0)
                        y_pred = np.argmax(model.predict(X), axis=-1)
                    
                    # Calculate accuracy
                    accuracy = accuracy_score(y, y_pred)
                    
                    # Convert predictions back to original labels for display
                    y_pred_labels = le.inverse_transform(y_pred)
                    y_true_labels = le.inverse_transform(y)
                    
                    # Display results
                    st.header("Model Performance")
                    st.success(f"Training complete! Model accuracy: {accuracy:.4f}")
                    
                    # Show confusion matrix
                    st.subheader("Confusion Matrix")
                    fig, ax = plt.subplots(figsize=(10, 8))
                    cm = confusion_matrix(y_true_labels, y_pred_labels)
                    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                              xticklabels=le.classes_,
                              yticklabels=le.classes_)
                    plt.xlabel('Predicted')
                    plt.ylabel('Actual')
                    st.pyplot(fig)
                    
                    # Show classification report
                    st.subheader("Classification Report")
                    report = classification_report(y_true_labels, y_pred_labels)
                    st.text(report)
                    
                    # Feature importance for tree-based models
                    if hasattr(model, 'feature_importances_'):
                        st.subheader("Feature Importance")
                        feature_importance = pd.DataFrame({
                            'Feature': X.columns,
                            'Importance': model.feature_importances_
                        }).sort_values('Importance', ascending=False)
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        sns.barplot(data=feature_importance, x='Importance', y='Feature')
                        plt.title('Feature Importance')
                        plt.xticks(rotation=45)
                        st.pyplot(fig)
                    
                    # Save model and preprocessing info
                    st.session_state['model'] = model
                    
                    # Save model to file
                    if not model_option == "Neural Network":
                        model_filename = f"{model_option.lower().replace(' ', '_')}_model.pkl"
                        joblib.dump(model, model_filename)
                        st.success(f"Model saved as {model_filename}")
                    
                except Exception as e:
                    st.error(f"Error during model training: {str(e)}")
                    st.error("Full error:", str(e.__class__.__name__))
                    import traceback
                    st.error(traceback.format_exc())
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")

else:
    st.info("Please upload a CSV file to begin training")

# Sidebar information
st.sidebar.header("🎯 Training Guide")
st.sidebar.markdown("""
### Model Selection Guide
1. **Random Forest**
   - Best for balanced performance
   - Good with mixed data types
   
2. **XGBoost**
   - Highest accuracy potential
   - Excellent feature importance
   
3. **Gradient Boosting**
   - Strong pattern detection
   - Robust to outliers
   
4. **Neural Network**
   - Best for complex patterns
   - Requires more data
""")