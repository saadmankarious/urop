import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

class UserSentiment:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text):
        sentiment = self.analyzer.polarity_scores(text)
        return sentiment['compound']

    def process_posts(self, posts):
        results = []
        for post in posts:
            sentiment_score = self.analyze_sentiment(post['selftext'])
            results.append({
                'username': post['author'],
                'post_id': post['id'],
                'compound_sentiment': sentiment_score,
                'created_utc': post['created_utc']
            })
        return results

    def aggregate_sentiment(self, results):
        df = pd.DataFrame(results)
        df['date'] = pd.to_datetime(df['created_utc'], unit='s').dt.strftime('%d.%m.%Y')
        positive_ratio = len(df[df['compound_sentiment'] > 0.05]) / len(df)
        negative_ratio = len(df[df['compound_sentiment'] < -0.05]) / len(df)
        average_sentiment = df['compound_sentiment'].mean()
        return positive_ratio, negative_ratio, average_sentiment

    def getBasicSentimentAnalysis(self, diagnosed_file_path, control_file_path):
        with open(diagnosed_file_path, 'r', encoding='utf-8') as diagnosed_file:
            diagnosed_data = json.load(diagnosed_file)
        with open(control_file_path, 'r', encoding='utf-8') as control_file:
            control_data = json.load(control_file)

        all_results = []
        
        # Process diagnosed users
        for user in diagnosed_data:
            user_posts = user['posts']
            results = self.process_posts(user_posts)
            positive_ratio, negative_ratio, average_sentiment = self.aggregate_sentiment(results)
            all_results.append({
                'label': 1,
                'username': user['username'],
                'positive_ratio': positive_ratio,
                'negative_ratio': negative_ratio,
                'average_sentiment': average_sentiment
            })
        
        # Process control users
        for user in control_data:
            for control in user['controls']:
                user_posts = control['posts']
                results = self.process_posts(user_posts)
                positive_ratio, negative_ratio, average_sentiment = self.aggregate_sentiment(results)
                all_results.append({
                    'label': 0,
                    'username': control['username'],
                    'positive_ratio': positive_ratio,
                    'negative_ratio': negative_ratio,
                    'average_sentiment': average_sentiment
                })
        
        result_df = pd.DataFrame(all_results)
        return result_df
