import json
import re
import argparse

# Function to load posts from JSON file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to load patterns from text file
def load_patterns(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to find self-diagnosed users
def find_self_diagnosed_users(posts, positive_patterns, negative_patterns, bipolar_synonyms):
    diagnosed_users = []
    unique_authors = set()

    for post in posts:
        text = post['selftext']  # Adjust based on your JSON structure
        author = post['author']

        if author in unique_authors:
            continue  # Skip if author is already processed

        bipolar_mentioned = False
        negative_diagnosis_mentioned = False
        positive_diagnosis_mentioned = False

        # Check for negative diagnosis patterns
        for pattern in negative_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                negative_diagnosis_mentioned = True
                break

        # Check for positive diagnosis patterns
        for pattern in positive_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                positive_diagnosis_mentioned = True
                start_pos = match.start()
                end_pos = match.end()

                # Calculate the distance between the positive pattern and bipolar mention
                for synonym in bipolar_synonyms:
                    synonym_match = re.search(r'\b' + re.escape(synonym) + r'\b', text, re.IGNORECASE)
                    if synonym_match:
                        synonym_start_pos = synonym_match.start()
                        synonym_end_pos = synonym_match.end()
                        distance = min(abs(start_pos - synonym_end_pos), abs(end_pos - synonym_start_pos))
                        if distance <= 40:
                            bipolar_mentioned = True
                            break

        # Only consider users who mention bipolar, don't mention negative diagnosis patterns,
        # mention positive diagnosis patterns, and satisfy the distance condition
        if bipolar_mentioned and not negative_diagnosis_mentioned and positive_diagnosis_mentioned:
            diagnosed_users.append(post)
            unique_authors.add(author)

    return diagnosed_users, list(unique_authors)

def main():
    parser = argparse.ArgumentParser(description='Identify diagnosed users based on their posts.')
    parser.add_argument('input_file', type=str, help='Path to the input JSON file containing cleaned posts')
    parser.add_argument('diagnosed_authors_file', type=str, help='Path to save the diagnosed authors JSON file')

    args = parser.parse_args()

    # Hardcoded paths to the pattern text files
    positive_patterns_file = '../resources/positive_diagnosis_patterns.txt'
    negative_patterns_file = '../resources/negative_diagnosis_patterns.txt'
    bipolar_synonyms_file = '../resources/bipolar_synonyms.txt'

    # Load the patterns and synonyms
    positive_patterns = load_patterns(positive_patterns_file)
    negative_patterns = load_patterns(negative_patterns_file)
    bipolar_synonyms = load_patterns(bipolar_synonyms_file)

    # Load posts data
    posts_data = load_json(args.input_file)
    print(f"Total posts loaded: {len(posts_data)}")

    # Find self-diagnosed users
    diagnosed_users, unique_authors = find_self_diagnosed_users(posts_data, positive_patterns, negative_patterns, bipolar_synonyms)
    print(f"Total diagnosed users found: {len(diagnosed_users)}")
    print(f"Total unique authors diagnosed: {len(unique_authors)}")

    # Save unique authors to a JSON file
    with open(args.diagnosed_authors_file, 'w') as f:
        json.dump(unique_authors, f, indent=4)
    print(f"Unique authors saved to {args.diagnosed_authors_file}")

if __name__ == '__main__':
    main()
