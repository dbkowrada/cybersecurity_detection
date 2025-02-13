# utils/preprocessing.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_data(df, is_training=True, encoders=None, scaler=None):
    """
    Preprocess the cybersecurity data.
    
    Args:
        df: Input DataFrame
        is_training: Whether this is training data
        encoders: Label encoders from training (for prediction)
        scaler: Standard scaler from training (for prediction)
    """
    # Define features to keep
    selected_features = [
        'Source Port', 'Destination Port', 'Packet Length', 
        'Anomaly Scores', 'Attack Signature', 'Source IP Address',
        'Destination IP Address', 'Payload Data', 'User Information',
        'Device Information', 'Geo-location Data', 'Proxy Information'
    ]
    
    # Add 'Attack Type' if it's training data
    if is_training and 'Attack Type' in df.columns:
        selected_features.append('Attack Type')
    
    # Select only available features
    available_features = [f for f in selected_features if f in df.columns]
    df_selected = df[available_features].copy()
    
    # Fill missing values
    for col in df_selected.columns:
        if df_selected[col].dtype == 'object':
            df_selected[col].fillna('unknown', inplace=True)
        else:
            df_selected[col].fillna(0, inplace=True)
    
    # Handle categorical features
    categorical_features = df_selected.select_dtypes(include=["object"]).columns
    label_encoders = {}
    
    for col in categorical_features:
        if is_training:
            # During training - fit and transform
            le = LabelEncoder()
            df_selected[col] = le.fit_transform(df_selected[col].astype(str))
            label_encoders[col] = le
        else:
            # During prediction - use encoders from training
            if encoders and col in encoders:
                le = encoders[col]
                try:
                    df_selected[col] = le.transform(df_selected[col].astype(str))
                except ValueError:
                    # Handle unseen labels
                    df_selected[col] = 0  # Default to 0 for unseen values
            else:
                # Fallback if encoder not found
                le = LabelEncoder()
                df_selected[col] = le.fit_transform(df_selected[col].astype(str))
    
    # Create interaction features
    if 'Source Port' in df_selected.columns and 'Anomaly Scores' in df_selected.columns:
        df_selected['Port_Anomaly_Interaction'] = df_selected['Source Port'] * df_selected['Anomaly Scores']
    
    if 'Packet Length' in df_selected.columns and 'Destination Port' in df_selected.columns:
        df_selected['Length_Port_Ratio'] = df_selected['Packet Length'] / (df_selected['Destination Port'] + 1)
    
    # Scale numerical features
    numerical_cols = df_selected.select_dtypes(include=['int64', 'float64']).columns
    if is_training:
        # During training - fit and transform
        scaler = StandardScaler()
        df_selected[numerical_cols] = scaler.fit_transform(df_selected[numerical_cols])
        return df_selected, label_encoders, scaler
    else:
        # During prediction - use scaler from training
        if scaler:
            df_selected[numerical_cols] = scaler.transform(df_selected[numerical_cols])
        else:
            # Fallback if scaler not found
            new_scaler = StandardScaler()
            df_selected[numerical_cols] = new_scaler.fit_transform(df_selected[numerical_cols])
        return df_selected, label_encoders

def get_feature_descriptions():
    """Return descriptions of features for the UI."""
    return {
        'Source Port': 'Port number of the source (0-65535)',
        'Destination Port': 'Port number of the destination (0-65535)',
        'Packet Length': 'Length of the packet in bytes',
        'Anomaly Scores': 'Anomaly score (0-1)',
        'Attack Signature': 'Signature of the attack pattern',
        'Source IP Address': 'Source IP address',
        'Destination IP Address': 'Destination IP address',
        'Payload Data': 'Data payload information',
        'User Information': 'User-related information',
        'Device Information': 'Device-related information',
        'Geo-location Data': 'Geographic location information',
        'Proxy Information': 'Proxy server information'
    }