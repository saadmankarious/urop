from datetime import datetime
import praw

# Function to convert Unix timestamp to a human-readable date
def convert_utc_to_date(utc_timestamp):
    return datetime.utcfromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')


# Authenticate with your credentials
reddit = praw.Reddit(
    client_id='NxgQ31Kx6oLAaqSrbg-yhg',
    client_secret='wstfr23DOlO-jOq4T-qNTcaJEAIkbg',
    user_agent='python:ADHDDataCollector:v0.1 (by /u/Otherwise-Idea-3537)'
)

# Example: Fetch posts from the r/bipolar subreddit
subreddit = reddit.subreddit('adhd')
print(subreddit.hot(limit=100))
for submission in subreddit.hot(limit=17000000):  # Change limit as needed
    created_date = convert_utc_to_date(submission.created_utc)
    print(f"Date Created: {created_date}\n")

# Example: Fetch comments from a specific post
#submission = reddit.submission(id='POST_ID')  # Replace 'POST_ID' with an 
#actual post ID
#submission.comments.replace_more(limit=0)  # Remove "load more comments"
#for comment in submission.comments.list():
#    print(comment.body)

