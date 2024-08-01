import json
import csv
import argparse
import re
import os
from collections import defaultdict

def preprocess_text(text):
    # Lowercasing Text
    text = text.lower()
    
    # Removing Hyperlinks
    text = re.sub(r'https?://\S+', '', text)
    
    # Removing HTML Tags
    text = re.sub(r'<.*?>', '', text)
    
    # Removing User Mentions
    text = re.sub(r'@\w+', '', text)
    
    # Removing HTML Entities
    text = re.sub(r'&\w+;', ' ', text)
    
    # Processing Hashtags
    text = re.sub(r'#(\w+)', r'\1', text)
    
    # Preserving Certain Characters and Whitespace
    text = re.sub(r'[^a-zA-Z0-9\s\.\'\!\?\,\;\-]', ' ', text)
    
    # Normalizing Spaces and Punctuation
    text = re.sub(r'(?<=[.,!?])(?=[^\s])', r' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(\.|\!|\?|\,|\;)\1+', r'\1', text)  # Deduplicate sentence-ending symbols
    text = re.sub(r'\.{3,}', '.', text)  # Replace consecutive ellipsis with a single full stop
    text = text.strip()
    text = re.sub(r'(?<=\w)([.,;])(?=\S)', r'\1 ', text)
    
    # Ensure post ends with a full stop if it doesn't end with a sentence-ending symbol
    if not re.search(r'[.!?]$', text):
        text += '.'
    
    return text

def load_json_files_from_folder(folder_path):
    json_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.startswith("matched_control_batch") and file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    
    data = []
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            data.extend(json.load(f))
    return data, len(json_files)

def format_to_csv(data, output_file, diagnosed_summary_file, control_threshold=None):
    total_posts = 0
    invalid_posts = 0
    duplicate_posts = 0
    seen_post_ids = set()
    diagnosed_counts = defaultdict(int)
    users_meeting_threshold = 0

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['TID', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in data:
            diagnosed_user = entry['diagnosed_user']
            controls = entry['controls']
            diagnosed_counts[diagnosed_user] += len(controls)
            if control_threshold is not None and diagnosed_counts[diagnosed_user] < control_threshold:
                continue
            users_meeting_threshold += 1
            for control in controls:
                control_user = control['username']
                posts = control['posts']
                for post in posts:
                    tid = f"0_{post['subreddit']}_{diagnosed_user}_{control_user}_{post['id']}"
                    text = post['selftext']
                    if text.strip():
                        if tid in seen_post_ids:
                            duplicate_posts += 1
                        else:
                            cleaned_text = preprocess_text(text)
                            writer.writerow({'TID': tid, 'text': cleaned_text})
                            seen_post_ids.add(tid)
                            total_posts += 1
                    else:
                        invalid_posts += 1

    # Write diagnosed user summary to a separate file
    with open(diagnosed_summary_file, 'w', newline='', encoding='utf-8') as summary_file:
        fieldnames = ['diagnosed_user', 'control_count']
        writer = csv.DictWriter(summary_file, fieldnames=fieldnames)

        writer.writeheader()
        for diagnosed_user, control_count in diagnosed_counts.items():
            if control_count >= control_threshold:
                writer.writerow({'diagnosed_user': diagnosed_user, 'control_count': control_count})

    return total_posts, invalid_posts, duplicate_posts, len(diagnosed_counts), users_meeting_threshold

def main():
    parser = argparse.ArgumentParser(description='Format JSON data to CSV and perform text cleaning.')
    parser.add_argument('input_folder', type=str, help='Path to the input folder containing JSON files')
    parser.add_argument('output_file', type=str, help='Path to the output CSV file')
    parser.add_argument('diagnosed_summary_file', type=str, help='Path to the output CSV file for diagnosed summary')
    parser.add_argument('--control_threshold', type=int, default=9, help='Minimum number of controls required to include a diagnosed user')

    args = parser.parse_args()

    data, file_count = load_json_files_from_folder(args.input_folder)
    total_posts, invalid_posts, duplicate_posts, unique_diagnosed_count, users_meeting_threshold = format_to_csv(data, args.output_file, args.diagnosed_summary_file, args.control_threshold)

    print(f"------------summary-----------")
    print(f"Number of files read: {file_count}")
    print(f"Total number of posts processed: {total_posts}")
    print(f"Number of invalid posts ignored: {invalid_posts}")
    print(f"Number of duplicate posts ignored: {duplicate_posts}")
    print(f"Number of unique diagnosed users: {unique_diagnosed_count}")
    print(f"Number of diagnosed users meeting the control threshold: {users_meeting_threshold}")

if __name__ == '__main__':
    main()
