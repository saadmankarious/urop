import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import time

# Use Agg backend for non-interactive environments
matplotlib.use('Agg')

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']

def process_json(file_path, username):
    # Load JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract posts for the given username
    user_posts = []
    for user_data in data:
        if user_data['username'] == username:
            for post in user_data['posts']:
                user_posts.append({
                    'post_id': post['id'],
                    'text': post['selftext'],
                    'created_utc': post['created_utc']
                })

    # Create a DataFrame
    df = pd.DataFrame(user_posts)

    # Analyze sentiment
    df['compound_sentiment'] = df['text'].apply(analyze_sentiment)

    # Convert timestamp to date
    df['date'] = pd.to_datetime(df['created_utc'], unit='s').dt.strftime('%d.%m.%Y')

    # Plot the results
    if not df.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(df['created_utc'], df['compound_sentiment'], marker='o')
        plt.xlabel('Time')
        plt.ylabel('Compound Sentiment Score')
        plt.title(f"Sentiment Scores Over Time for {username}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the plot as a file
        plot_filename = f"{username}_sentiment_plot.png"
        plt.savefig(plot_filename)
        print(f"Plot saved as {plot_filename}")

        print(f"Posts and sentiment scores for user: {username}")
        print(df[['post_id', 'compound_sentiment', 'date']].to_string(index=False))
    else:
        print(f"No posts found for user: {username}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze sentiment of user posts from a JSON file.')
    parser.add_argument('file_path', type=str, help='Path to the JSON file')
    parser.add_argument('username', type=str, help='Username to filter posts by')
    args = parser.parse_args()

    process_json(args.file_path, args.username)
