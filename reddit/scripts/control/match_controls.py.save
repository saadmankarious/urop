import json
import requests
import argparse
import urllib3
import re
import time

# Suppress only the single InsecureRequestWarning from urllib3 needed to remove warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_patterns(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file.readlines()]


def fetch_user_submissions(username):
    url = f'https://arctic-shift.photon-reddit.com/api/posts/search?author={username}&limit=auto'
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch submissions for user {username}. Error: {e}")
        return []


def is_valid_selftext(selftext):
    invalid_patterns = [
        r'^\[deleted\]$',        # Exactly "[deleted]"
        r'^\[removed\]$',        # Exactly "[removed]"
        r'\[deleted\]',          # Contains "[deleted]"
        r'\[removed\]',          # Contains "[removed]"
        r'^\s*$',                # Empty or whitespace-only
        r'\[View Poll\]\(https://www.reddit.com/poll/.*\)'  # Poll link pattern
    ]
    for pattern in invalid_patterns:
        if re.search(pattern, selftext, re.IGNORECASE):
            return False
    return True


def contains_mental_health_patterns(text, patterns):
    text = text.lower()
    return any(re.search(pattern, text) for pattern in patterns)


def filter_and_simplify_posts(posts, mental_health_patterns, mental_health_subreddits):
    # Define relevant properties to keep
    relevant_properties = ['id', 'title', 'selftext',
                           'author', 'created_utc', 'subreddit', 'score']

    simplified_posts = []
    for post in posts:
        selftext = post.get('selftext', '')
        subreddit = post.get('subreddit', '').lower()

        if subreddit in mental_health_subreddits:
            return []
        if contains_mental_health_patterns(selftext, mental_health_patterns):
            return []
        
        if is_valid_selftext(selftext):
            simplified_post = {prop: post[prop] for prop in relevant_properties if prop in post}
            simplified_posts.append(simplified_post)

    return simplified_posts


def filter_control_users(diagnosed_users, mental_health_subreddits, mental_health_patterns, min_controls=9):
    matched_controls = []
    matched_diagnosed_count = 0
    used_controls = set()

    for diagnosed_user in diagnosed_users:
        diagnosed_username = diagnosed_user['username']
        diagnosed_post_count = diagnosed_user['post_count']
        candidate_usernames = diagnosed_user['candidate_usernames']
        min_posts = max(1, diagnosed_post_count // 2)
        max_posts = diagnosed_post_count * 2

        selected_controls = []
        for candidate in candidate_usernames:
            if len(selected_controls) >= min_controls:
                break
            if candidate in used_controls:
                continue
            submissions = fetch_user_submissions(candidate)
            cleaned_posts = filter_and_simplify_posts(submissions, mental_health_patterns, mental_health_subreddits)

            if len(cleaned_posts) == 0:
                print(f"Candidate {candidate} does not meet exclusion criteria.")
                continue

            if len(cleaned_posts) < 50:
                print(f"Skipping candidate {candidate} with few posts {len(submissions)}")
                continue

            if min_posts < len(cleaned_posts) < max_posts:
                selected_controls.append({
                    'username': candidate,
                    'post_count':  len(cleaned_posts),
                    'posts': cleaned_posts
                })
                used_controls.add(candidate)

        if len(selected_controls) >= min_controls:
            matched_diagnosed_count += 1

        matched_controls.append({
            'diagnosed_user': diagnosed_username,
            'diagnosed_post_count': diagnosed_post_count,
            'controls': selected_controls[:min_controls]
        })

        print(f"Matched {len(selected_controls)} controls for diagnosed user {diagnosed_username}")

    total_diagnosed_count = len(diagnosed_users)
    print(f"Total diagnosed users matched: {matched_diagnosed_count} out of {total_diagnosed_count}")

    return matched_controls


def main():
    parser = argparse.ArgumentParser(
        description='Match diagnosed users with control users.')
    parser.add_argument('input_file', type=str,
                        help='Path to the input JSON file containing expanded diagnosed users')
    parser.add_argument('output_file', type=str,
                        help='Path to save the matched controls JSON file')
    parser.add_argument('--min_controls', type=int, default=9,
                        help='Minimum number of control users to match for each diagnosed user')

    args = parser.parse_args()

    start_time = time.time()

    diagnosed_users = load_json(args.input_file)
    mental_health_subreddits = load_patterns('../resources/mh_subreddits.txt')
    mental_health_patterns = load_patterns('../resources/mh_patterns.txt')
    matched_controls = filter_control_users(
        diagnosed_users, mental_health_subreddits, mental_health_patterns, args.min_controls)

    with open(args.output_file, 'w', encoding='utf-8') as file:
        json.dump(matched_controls, file, indent=4)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Matched controls data saved to {args.output_file}")
    print(f"Time taken for matching: {elapsed_time:.2f} seconds")


if __name__ == '__main__':
    main()
