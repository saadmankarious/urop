import praw
import datetime
import json
import argparse
import os
import time

# Authenticate with your credentials
reddit = praw.Reddit(
    client_id='NxgQ31Kx6oLAaqSrbg-yhg',
    client_secret='wstfr23DOlO-jOq4T-qNTcaJEAIkbg',
    user_agent='python:ADHDDataCollector:v0.1 (by /u/Otherwise-Idea-3537)'
)

# Function to fetch posts
def fetch_posts(subreddit_name, limit=100, after=None):
    subreddit = reddit.subreddit(subreddit_name)
    return list(subreddit.new(limit=limit, params={'after': after}))

def main():
    parser = argparse.ArgumentParser(description='Fetch Reddit posts from a specified subreddit.')
    parser.add_argument('subreddit', type=str, help='The subreddit to fetch posts from')
    args = parser.parse_args()

    subreddit_name = args.subreddit
    limit_per_request = 100  # Number of posts per request
    iterations = 20  # Number of iterations (you can adjust this based on your needs)
    after = None
    base_output_dir = f'../script_output/reddit_native_api/{subreddit_name}'

    # Create the output directory if it doesn't exist
    os.makedirs(base_output_dir, exist_ok=True)

    total_posts = 0

    # Loop to fetch multiple sets of posts
    for iteration in range(iterations):
        posts = fetch_posts(subreddit_name, limit_per_request, after)
        posts_data = []

        # Access the last post directly
        last_post = posts[-1] if posts else None

        for post in posts:
            if post.selftext and len(post.selftext) > 0:  # Filter posts with only selftext
                post_data = {
                    "id": post.id,
                    "title": post.title,
                    "selftext": post.selftext,
                    "author": str(post.author),
                    "created_utc": datetime.datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                }
                posts_data.append(post_data)

        # Update the 'after' parameter to fetch the next set of posts
        after = last_post.fullname if last_post else after

        # Save the posts to a JSON file with a timestamp and subreddit naming
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        output_file = os.path.join(base_output_dir, f'{subreddit_name}_{timestamp}_{iteration+1}.json')
        with open(output_file, 'w') as f:
            json.dump(posts_data, f, indent=4)

        total_posts += len(posts_data)
        print(f"Iteration {iteration+1}: Saved {len(posts_data)} posts to {output_file}")

        # Break the loop if no posts were fetched
        if not last_post:
            print("No more posts to fetch.")
            break

        # Respect Reddit's API rate limits
        time.sleep(1)  # Adjust this sleep time as needed to respect the rate limits

    print(f"Total posts fetched: {total_posts}")

if __name__ == '__main__':
    main()

