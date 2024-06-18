# fetches a number of reddit posts that matches a given pattern
# EX: python fetch_reddit_posts.py "I was diagnosed with" --limit 10 --output reddit_posts.json

import os
import json
import argparse
from datetime import datetime
from google.cloud import bigquery

# Initialize the BigQuery client
client = bigquery.Client(project='hours-delivery')

# Function to convert Unix timestamp to a human-readable date


def convert_utc_to_date(utc_timestamp):
    return datetime.utcfromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')


dates = [
    '2015_12',
    '2016_01',
    '2016_02',
    '2016_03',
    '2016_04',
    '2016_05',
    '2016_06',
    '2016_07',
    '2016_08',
    '2016_09',
    '2016_10',
    '2016_11',
    '2016_12',
    '2017_01',
    '2017_02',
    '2017_03',
    '2017_04',
    '2017_05',
    '2017_06',
    '2017_07',
    '2017_08',
    '2017_09',
    '2017_10',
    '2017_11',
    '2017_12',
    '2018_01',
    '2018_02',
    '2018_03',
    '2018_04',
    '2018_05',
    '2018_06',
    '2018_07',
    '2018_08',
    '2018_09',
    '2018_10',
    '2018_11',
    '2018_12',
    '2019_01',
    '2019_02',
    '2019_03',
    '2019_04',
    '2019_05',
    '2019_06',
    '2019_07',
    '2019_08',
]

# Function to fetch and process posts based on a given pattern


def fetch_and_process_posts(condition, date):
    query = f"""
    SELECT id, title, selftext, author, created_utc
    FROM `fh-bigquery.reddit_posts.{date}`
    WHERE subreddit = '{condition}'
    ORDER BY created_utc DESC
    """

    query_job = client.query(query)
    results = query_job.result()
    posts = []

    for row in results:
        post_data = {
            'id': row.id,
            'title': row.title,
            'selftext': row.selftext,
            'author': row.author,
            'created_utc': convert_utc_to_date(row.created_utc)
        }
        posts.append(post_data)

    return posts

# Function to save posts to a JSON file


def save_posts_to_json(posts, filename):
    filename = '../script_output/fh-bigquery/' + filename + '.json'
    with open(filename, 'w') as f:
        json.dump(posts, f, indent=4)
    print(f"Saved {len(posts)} posts to {filename}")

# Main function to parse arguments and call fetch_and_process_posts


def main():
    parser = argparse.ArgumentParser(
        description='Fetch and save Reddit posts matching a specific pattern.')
    parser.add_argument('--condition', type=str, default='bipolar',
                        help='The number of posts to fetch (default: 10)')
    args = parser.parse_args()

    total_posts = 0
    print(f'milking {args.condition} posts...')
    
    for date in dates:
        posts = fetch_and_process_posts(condition=args.condition, date=date)
        save_posts_to_json(posts, filename=args.condition + '/' + date)
        total_posts = total_posts + len(posts)
        
    print('=================YAAAI!==================')
    print(f'done milking {total_posts} reddit posts for {args.condition}!')


if __name__ == '__main__':
    main()
