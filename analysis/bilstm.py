import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Bidirectional, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import argparse

# Load and preprocess the data
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    
    # Extract and process the 'tid' column
    df[['diagnosed', 'userID', 'postID']] = df['tid'].apply(lambda x: pd.Series(parse_tid(x)))
    df['MHC'] = df['diagnosed'].apply(lambda x: 'bipolar' if x == '1' else 'control')
    print(df.head(100))

    df.drop(columns=['tid', 'postID', 'diagnosed'], inplace=True)
    # Split into features and target
    X = df.drop(columns=['MHC', 'userID'])
    y = df['MHC']
    
    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y, df['userID']

# Parse the 'tid' column to extract diagnosed, userID, and postID
def parse_tid(tid):
    parts = tid.split('_')
    diagnosed = parts[0]
    post_id = parts[-1]
    user_id = '_'.join(parts[1:-1])
    return diagnosed, user_id, post_id

# Build the BiLSTM model
def build_bilstm_model(input_shape):
    model = Sequential()
    model.add(Bidirectional(LSTM(128, return_sequences=True), input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(64)))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Train and evaluate the BiLSTM model
def train_and_evaluate_bilstm(X_train, y_train, X_test, y_test):
    input_shape = (X_train.shape[1], 1)
    
    model = build_bilstm_model(input_shape)
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
    
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, callbacks=[early_stopping])
    
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy:.4f}")
    
    return model, history

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a BiLSTM model on mental health data.')
    parser.add_argument('input_file', type=str, help='Path to the CSV file containing the data')
    args = parser.parse_args()

    # Load and preprocess the data
    X, y, user_ids = load_and_preprocess_data(args.input_file)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test, user_train, user_test = train_test_split(X, y, user_ids, test_size=0.2, stratify=y, random_state=42)

    # Ensure there is no overlap in userID between training and testing sets
    assert len(set(user_train).intersection(set(user_test))) == 0, f"Data leakage detected: Overlapping userIDs in train and test sets: {len(set(user_train).intersection(set(user_test))) }"

    # Check class distribution in training and test sets
    print(f"Training set class distribution:\n{pd.Series(y_train).value_counts()}")
    print(f"Test set class distribution:\n{pd.Series(y_test).value_counts()}")

    # Train and evaluate the BiLSTM model
    model, history = train_and_evaluate_bilstm(X_train, y_train, X_test, y_test)

    # Save the trained model
    model.save('bilstm_model.h5')
