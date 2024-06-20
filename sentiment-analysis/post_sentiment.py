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

def process_diagnosed(file_path, username, control=False):
    # Load JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    user_posts = []
    if control:
        # Extract posts for the given username in control format
        for user_data in data:
                for control_user in user_data['controls']:
                    if control_user['username'] == username:
                        for post in control_user['posts']:
                            user_posts.append({
                                'post_id': post['id'],
                                'text': post['selftext'],
                                'created_utc': post['created_utc']
                            })
    else:
        # Extract posts for the given username in the original format
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
    print(user_posts)

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

def process_controls(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    all_user_posts = []
    for user_data in data:
        username = user_data['username']
        for post in user_data['posts']:
            if post['created_utc'] >= 1514764800:  # 01.01.2018
                all_user_posts.append({
                    'username': username,
                    'post_id': post['id'],
                    'text': post['selftext'],
                    'created_utc': post['created_utc']
                })

    df = pd.DataFrame(all_user_posts)
    df['compound_sentiment'] = df['text'].apply(analyze_sentiment)
    df['date'] = pd.to_datetime(df['created_utc'], unit='s').dt.strftime('%d.%m.%Y')

    if not df.empty:
        aggregated_df = df.groupby('date')['compound_sentiment'].mean().reset_index()
        plt.figure(figsize=(10, 5))
        plt.plot(aggregated_df['date'], aggregated_df['compound_sentiment'], marker='o')
        plt.xlabel('Time')
        plt.ylabel('Average Compound Sentiment Score')
        plt.title("Average Sentiment Scores Over Time for All Users")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plot_filename = "all_users_sentiment_plot.png"
        plt.savefig(plot_filename)
        print(f"Aggregated plot saved as {plot_filename}")
    else:
        print("No posts found for any user.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze sentiment of user posts from a JSON file.')
    parser.add_argument('file_path', type=str, help='Path to the JSON file')
    parser.add_argument('username', type=str, help='Username to filter posts by')
    parser.add_argument('--control', action='store_true', help='Specify if the input file is in the control format')
    parser.add_argument('--all', action='store_true', help='Analyze sentiment for all users in the file')

    args = parser.parse_args()

    if args.all:
        process_controls(args.file_path)
    else:
        process_diagnosed(args.file_path, args.username, args.control)
