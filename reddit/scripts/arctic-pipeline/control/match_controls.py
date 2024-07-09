import json
import requests
import argparse
import urllib3
import re
import time

def globalSettings(settings_file='../../../../config/global.json'):
    with open(settings_file, 'r', encoding='utf-8') as file:
        settings = json.load(file)
    return settings

# Suppress only the single InsecureRequestWarning from urllib3 needed to remove warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_patterns(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file.readlines()]

def fetch_user_submissions(username):
    posts_url = f'https://arctic-shift.photon-reddit.com/api/posts/search?author={username}&limit=auto'
    comments_url = f'https://arctic-shift.photon-reddit.com/api/comments/search?author={username}&limit=auto'
    posts, comments = [], []

    try:
        # Fetch posts
        posts_response = requests.get(posts_url, verify=False)
        posts_response.raise_for_status()
        posts = posts_response.json().get('data', [])
        
        # Fetch comments
        comments_response = requests.get(comments_url, verify=False)
        comments_response.raise_for_status()
        comments = comments_response.json().get('data', [])
        
        # Adjust comments to use 'selftext' instead of 'body'
        for comment in comments:
            comment['selftext'] = comment.pop('body', '')

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch submissions for user {username}. Error: {e}")
        return []

    return posts + comments

def is_valid_selftext(selftext):
    invalid_patterns = [
        r'^\[deleted\]$',        # Exactly "[deleted]"
        r'^\[removed\]$',        # Exactly "[removed]"
        r'\[deleted\]',          # Contains "[deleted]"
        r'\[removed\]',          # Contains "[removed]"
        r'^\s*$',                # Empty or whitespace-only
        r'\[View Poll\]\(https://www.reddit.com/poll/.*\)',  # Poll link pattern
        r'https?://\S+',         # Contains a URL
        r'[^a-zA-Z0-9\s\.\'\!\?\,\;\-]'  # Non-English characters
    ]
    for pattern in invalid_patterns:
        if re.search(re.escape(pattern), selftext, re.IGNORECASE):
            return False

    # Check if there is at least one sentence-ending punctuation mark
    if not re.search(r'[.!?]', selftext):
        return False

    # Check if the sentence is too short (one or two words)
    sentences = re.split(r'[.!?]', selftext)
    for sentence in sentences:
        words = sentence.strip().split()
        if len(words) > 10:
            return True

    return False

def contains_mental_health_patterns(text, patterns):
    text = text.lower()
    return any(re.search(re.escape(pattern), text) for pattern in patterns)

def filter_and_simplify_posts(posts, mental_health_patterns, mental_health_subreddits):
    # Define relevant properties to keep
    relevant_properties = ['id', 'title', 'selftext', 'author', 'created_utc', 'subreddit', 'score']
    simplified_posts = []
    seen_selftexts = set()

    for post in posts:
        selftext = post.get('selftext', '')
        subreddit = post.get('subreddit', '').lower() if post.get('subreddit') else ''

        if subreddit in mental_health_subreddits or contains_mental_health_patterns(selftext, mental_health_patterns):
            return []

        if is_valid_selftext(selftext) and selftext not in seen_selftexts:
            simplified_post = {prop: post[prop] for prop in relevant_properties if prop in post}
            simplified_posts.append(simplified_post)
            seen_selftexts.add(selftext)

    return simplified_posts

def fetch_and_filter(candidate, mental_health_patterns, mental_health_subreddits):
    submissions = fetch_user_submissions(candidate)
    cleaned_posts = filter_and_simplify_posts(submissions, mental_health_patterns, mental_health_subreddits)
    return candidate, cleaned_posts

def filter_control_users(diagnosed_users, mental_health_subreddits, mental_health_patterns, output_directory, min_controls=9, output_prefix='matched_controls'):
    matched_controls = []
    matched_diagnosed_count = 0
    used_controls = set()
    not_meeting_post_count = 0
    not_meeting_exclusion_criteria = 0
    batch_index = 0

    def save_batch(batch_index, matched_controls):
        output_file = f"{output_directory}/{output_prefix}_batch_{batch_index}.json"
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(matched_controls, file, indent=4)
        print(f"Batch {batch_index} saved with {len(matched_controls)} matched controls")

    for diagnosed_index, diagnosed_user in enumerate(diagnosed_users, start=1):
        diagnosed_username = diagnosed_user['username']
        diagnosed_post_count = diagnosed_user['post_count']
        candidate_usernames = diagnosed_user['candidate_usernames']
        min_posts = max(1, diagnosed_post_count // 2)
        max_posts = diagnosed_post_count * 2

        selected_controls = []
        for candidate in candidate_usernames:
            try:
                candidate, cleaned_posts = fetch_and_filter(candidate, mental_health_patterns, mental_health_subreddits)
                if candidate in used_controls:
                    continue

                if len(cleaned_posts) == 0:
                    not_meeting_exclusion_criteria += 1
                    continue

                if len(cleaned_posts) < 50:
                    not_meeting_post_count += 1
                    continue

                if min_posts < len(cleaned_posts) < max_posts:
                    selected_controls.append({
                        'username': candidate,
                        'post_count': len(cleaned_posts),
                        'posts': cleaned_posts
                    })
                    used_controls.add(candidate)

                if len(selected_controls) >= min_controls:
                    break

            except Exception as e:
                print(f"Error processing candidate {candidate}: {e}")

        if len(selected_controls) >= min_controls:
            matched_diagnosed_count += 1

        matched_controls.append({
            'diagnosed_user': diagnosed_username,
            'diagnosed_post_count': diagnosed_post_count,
            'controls': selected_controls[:min_controls]
        })
        print(f"Matched {diagnosed_index} out of {len(diagnosed_users)} diagnosed users")

        if len(matched_controls) >= globalSettings()["control_batch_size"]:
            batch_index += 1
            save_batch(batch_index, matched_controls)
            matched_controls = []
            print("")
            print(f"Batch {batch_index} completed and saved. Processed {diagnosed_index} out of {len(diagnosed_users)} diagnosed users.")

    if matched_controls:
        batch_index += 1
        save_batch(batch_index, matched_controls)
        print("")
        print(f"Batch {batch_index} completed and saved. Processed all diagnosed users.")

    total_diagnosed_count = len(diagnosed_users)
    print(f"Total diagnosed users matched: {matched_diagnosed_count} out of {total_diagnosed_count}")
    print(f"Candidates not meeting post count: {not_meeting_post_count}")
    print(f"Candidates not meeting exclusion criteria: {not_meeting_exclusion_criteria}")

def main():
    parser = argparse.ArgumentParser(description='Match diagnosed users with control users.')
    parser.add_argument('input_file', type=str, help='Path to the input JSON file containing expanded diagnosed users')
    parser.add_argument('output_directory', type=str, help='Directory to save the output JSON files')
    parser.add_argument('--output_prefix', type=str, default='matched_control', help='Prefix for the output JSON files')
    parser.add_argument('--min_controls', type=int, default=9, help='Minimum number of control users to match for each diagnosed user')

    args = parser.parse_args()

    start_time = time.time()

    diagnosed_users = load_json(args.input_file)
    mental_health_subreddits = load_patterns('../../../resources/mh_subreddits.txt')
    mental_health_patterns = load_patterns('../../../resources/mh_patterns.txt')
    filter_control_users(diagnosed_users, mental_health_subreddits, mental_health_patterns, args.output_directory, globalSettings()["controls_per_diagnosed"], args.output_prefix)

    end_time = time.time()
    elapsed_time = (end_time - start_time)/60

    print(f"Time taken for matching: {elapsed_time:.2f} m")

if __name__ == '__main__':
    main()
