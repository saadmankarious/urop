from datetime import datetime
import praw
import json
import argparse

# Function to convert Unix timestamp to a human-readable date
def convert_utc_to_date(utc_timestamp):
    return datetime.utcfromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Authenticate with your PRAW credentials
reddit = praw.Reddit(
    client_id='NxgQ31Kx6oLAaqSrbg-yhg',
    client_secret='wstfr23DOlO-jOq4T-qNTcaJEAIkbg',
    user_agent='python:ADHDDataCollector:v0.1 (by /u/Otherwise-Idea-3537)'
)

# Function to fetch and save posts from a specific subreddit within a date range
def fetch_and_save_posts(subreddit_name, start_date, end_date, limit=100):
    subreddit = reddit.subreddit(subreddit_name)
    start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
    end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
    
    posts = []
    count = 0
    total_comments = 0

    # Use PRAW's `new` method with pagination
    for submission in subreddit.new(limit=None):
        submission_timestamp = int(submission.created_utc)
        
        if start_timestamp <= submission_timestamp <= end_timestamp:
            total_comments += submission.num_comments
            post_data = {
                'id': submission.id,
                'title': submission.title,
                'selftext': submission.selftext,
                'author': str(submission.author),
                'score': submission.score,
                'url': submission.url,
                'created_utc': convert_utc_to_date(submission.created_utc),
                'num_comments': submission.num_comments,
                'subreddit': str(submission.subreddit),
                'permalink': submission.permalink
            }
            posts.append(post_data)
            count += 1
            if count >= limit:
                break
    
    # Save the posts to a JSON file
    filename = f'../script_output/reddit_native_api/{subreddit_name}/{subreddit_name}_{start_date}_to_{end_date}.json'
    with open(filename, 'w') as f:
        json.dump(posts, f, indent=4)
    
    print(f"Saved {len(posts)} posts from r/{subreddit_name} to {filename}")
    print(f"Total number of comments collected: {total_comments}")

# Main function to parse arguments and call fetch_and_save_posts
def main():
    parser = argparse.ArgumentParser(description='Fetch and save Reddit posts within a specific time frame.')
    parser.add_argument('subreddit', type=str, help='The subreddit to fetch posts from')
    parser.add_argument('start_date', type=str, help='The start date in YYYY-MM-DD format')
    parser.add_argument('end_date', type=str, help='The end date in YYYY-MM-DD format')
    parser.add_argument('--limit', type=int, default=100, help='The number of posts to fetch (default: 100)')
    args = parser.parse_args()

    fetch_and_save_posts(args.subreddit, args.start_date, args.end_date, limit=args.limit)

if __name__ == '__main__':
    main()
