import json
import re
import argparse

# Function to check if selftext is valid
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

# Function to filter and simplify posts
def filter_and_simplify_posts(input_file, output_file):
    # Define relevant properties to keep
    relevant_properties = ['id', 'title', 'selftext', 'author', 'created_utc', 'subreddit', 'score']

    simplified_user_submissions = []
    unique_texts = set()
    total_simplified_posts = 0
    total_length = 0
    duplicate_count = 0

    # Read the large JSON file line by line
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            post = json.loads(line.strip())
            selftext = post.get('selftext', '')
            if is_valid_selftext(selftext):
                cleaned_text = preprocess_text(selftext)
                if cleaned_text in unique_texts:
                    duplicate_count += 1
                    continue
                unique_texts.add(cleaned_text)
                simplified_post = {prop: post[prop] for prop in relevant_properties if prop in post}
                simplified_user_submissions.append(simplified_post)
                total_length += len(selftext)
                total_simplified_posts += 1

    # Save the simplified posts to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(simplified_user_submissions, file, indent=4)

    print(f"Posts read: {total_simplified_posts}")
    print(f"Duplicated posts: {duplicate_count}")

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

def main():
    parser = argparse.ArgumentParser(
        description='Filter and simplify user submissions JSON file for NLP projects.')
    parser.add_argument('input_file', type=str,
                        help='Path to the input JSON file containing all user submissions')
    parser.add_argument('output_file', type=str,
                        help='Path to save the simplified JSON file')

    args = parser.parse_args()

    filter_and_simplify_posts(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
