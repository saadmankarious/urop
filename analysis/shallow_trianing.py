import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from sklearn.model_selection import train_test_split
import argparse

def parse_tid(tid):
    parts = tid.split('_')
    diagnosed = parts[0]
    if diagnosed == '0':
        # Format: 0_subreddit_diagnosedUsername_controlUsername_postID
        post_id = parts[-1]
        user_id = parts[-2]  # control username
    else:
        # Format: 1_username_postID
        post_id = parts[-1]
        user_id = '_'.join(parts[1:-1])  # diagnosed username
    return diagnosed, user_id, post_id

def preprocess_data(df):
    print(df.head())
    print(df.tail())
    df[['diagnosed', 'userID', 'postID']] = df['tid'].apply(lambda x: pd.Series(parse_tid(x)))
    df['MHC'] = df['diagnosed'].apply(lambda x: 'bipolar' if x == '1' else 'control')
    df.drop(columns=['tid', 'postID', 'diagnosed'], inplace=True)
    print('after getting post id')
    print(df.head())
    print(df.tail())
    return df

# Function to load and preprocess dataset
def load_and_preprocess_dataset(dataset_path):
    df = pd.read_csv(dataset_path)
    df = preprocess_data(df)
    
    # Assuming 'MHC' is the target column
    X = df.drop(columns=['MHC', 'userID'])  # Adjust columns to drop as needed
    y = df['MHC']
    
    # Standard scaling of features if necessary
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, X, y

# Function to train and evaluate models using dedicated training and test datasets
def train_and_evaluate_models(X_train, y_train, X_test, y_test, dataset_name):
    results_df = pd.DataFrame(columns=['Model', 'Dataset', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'Confusion Matrix'])
    
    for name, model in models.items():
        print(f"Training and evaluating {name}...")
        
        # Train the model on the training data
        model.fit(X_train, y_train)
        
        # Predict on the test data
        y_pred = model.predict(X_test)
        
        # Calculate evaluation metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision, recall, fscore, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        confusion_matrix_result = confusion_matrix(y_test, y_pred)
        
        # Append results to DataFrame
        temp_df = pd.DataFrame({
            'Model': [name],
            'Dataset': [dataset_name],
            'Accuracy': [accuracy],
            'Precision': [precision],
            'Recall': [recall],
            'F1-Score': [fscore],
            'Confusion Matrix': [confusion_matrix_result]
        })
        results_df = pd.concat([results_df, temp_df], ignore_index=True)
    
    return results_df

# Define models dictionary globally
models = {
    "Random Forest": RandomForestClassifier(random_state=42),
    "SVM": SVC(random_state=42, probability=True),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
    "MLP Classifier": MLPClassifier(random_state=42),
    "AdaBoost": AdaBoostClassifier(random_state=42)
}

def main():
    parser = argparse.ArgumentParser(description='Run model analysis on dataset.')
    parser.add_argument('input_directory', type=str, help='Path to the input directory containing the CSV file')
    args = parser.parse_args()

    input_file_path = os.path.join(args.input_directory, 'chunky_03.csv')

    # Load and preprocess the dataset
    print(f"\nProcessing dataset: {input_file_path}")
    X_scaled, X_raw, y = load_and_preprocess_dataset(input_file_path)

    # Log some samples from each class
    print("\nSample data from 'bipolar' class:")
    print(X_raw[y == 'bipolar'].head())
    print("\nSample data from 'control' class:")
    print(X_raw[y == 'control'].head())

    # Perform the train-test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, stratify=y, random_state=42)

    # Ensure there are more than one class in y_train and y_test
    assert len(y_train.unique()) > 1, "The training dataset must contain more than one class."
    assert len(y_test.unique()) > 1, "The test dataset must contain more than one class."

    # Log the distribution of classes in the training and test sets
    print(f"\nTraining set class distribution:\n{y_train.value_counts()}")
    print(f"Test set class distribution:\n{y_test.value_counts()}")

    # Train and evaluate models
    results_df = train_and_evaluate_models(X_train, y_train, X_test, y_test, "bipolar")

    # Write results to a CSV file
    results_df.to_csv("bipolar_model_evaluation_results.csv", index=False)
    print(results_df.head())

if __name__ == '__main__':
    main()
