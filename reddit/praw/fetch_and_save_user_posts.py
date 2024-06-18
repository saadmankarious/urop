import praw
import json
import argparse
from datetime import datetime
import os

# Authenticate with your credentials
reddit = praw.Reddit(
    client_id='NxgQ31Kx6oLAaqSrbg-yhg',
    client_secret='wstfr23DOlO-jOq4T-qNTcaJEAIkbg',
    user_agent='python:ADHDDataCollector:v0.1 (by /u/Otherwise-Idea-3537)'
)

# Function to convert Unix timestamp to a human-readable date


def convert_utc_to_date(utc_timestamp):
    return datetime.utcfromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Function to fetch and save submissions and comments by a specific username


def fetch_and_save_user_data(username):
    user = reddit.redditor(username)
    user_data = {
        "submissions": [],
        "comments": []
    }

    # Fetch the user's submissions
    for submission in user.submissions.new(limit=None):
        submission_data = {
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
        user_data["submissions"].append(submission_data)


    output_dir = 'script_output/users'
    os.makedirs(output_dir, exist_ok=True)

    # Save the user data to a JSON file
    output_file = os.path.join(output_dir, f'{username}_data.json')
    if user_data:
        with open(output_file, 'w') as f:
            json.dump(user_data, f, indent=4)
        print(f"Saved {len(user_data['submissions'])} submissions to the directory at {output_file}")
    else:
        print(f"no data found for user {username}")

# Main function to parse arguments and call fetch_and_save_user_data


def main():
    parser = argparse.ArgumentParser(
        description='Fetch and save Reddit data (submissions and comments) by a specific username.')
    parser.add_argument('username', type=str,
                        help='The Reddit username whose data to fetch')
    args = parser.parse_args()

    fetch_and_save_user_data(args.username)


if __name__ == '__main__':
    main()
