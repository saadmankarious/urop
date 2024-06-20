
import UserSentiment
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

def main():
    diagnosed_file_path = '../../reddit/scripts/bipolar-24_output/diagnosed/data-diagnosed.final.json'  # Replace with your actual file path
    control_file_path = '../../reddit/scripts/bipolar-24_output/control/data-control.final.json'      # Replace with your actual file path

    sentiment_analyzer = UserSentiment.UserSentiment()
    df = sentiment_analyzer.getBasicSentimentAnalysis(diagnosed_file_path, control_file_path)
    print(df)

    # Prepare features and labels
    X = df[['positive_ratio', 'negative_ratio', 'average_sentiment']]  # Features
    y = df['label']  # Labels

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize the RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the classifier
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Evaluate the classifier
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(report)

    return clf  # Return the trained classifier

def predict_labels(clf, input_data):
    """
    Predict class labels for input data using the trained classifier.

    :param clf: Trained RandomForestClassifier
    :param input_data: DataFrame with the same structure as the training features
    :return: Predicted class labels
    """
    predictions = clf.predict(input_data)
    return predictions

if __name__ == "__main__":
    # Train the model and get the classifier
    trained_classifier = main()

    # Example usage of the predict_labels function
    example_input = pd.DataFrame({
        'positive_ratio': [0.5, 0.7],
        'negative_ratio': [0.3, 0.2],
        'average_sentiment': [0.1, 0.4]
    })

    predicted_labels = predict_labels(trained_classifier, example_input)
    print("Predicted Labels:", predicted_labels)
