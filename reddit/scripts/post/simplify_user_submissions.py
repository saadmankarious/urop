# to optimize all submissions file size on disk, cast only relevant submission properties
import json
import argparse

# Function to simplify posts by retaining only relevant properties
def simplify_posts(input_file, output_file):
    # Define relevant properties to keep
    relevant_properties = ['id', 'title', 'selftext', 'author', 'created_utc', 'subreddit', 'score']

    # Load the large JSON file
    with open(input_file, 'r', encoding='utf-8') as file:
        all_user_submissions = json.load(file)

    # Simplify the posts
    simplified_user_submissions = []
    total_simplified_posts = 0
    for user_data in all_user_submissions:
        simplified_posts = []
        for post in user_data['posts']:
            simplified_post = {prop: post[prop] for prop in relevant_properties if prop in post}
            simplified_posts.append(simplified_post)
        
        simplified_user_data = {
            'username': user_data['username'],
            'posts': simplified_posts
        }
        total_simplified_posts += len(simplified_posts)
        simplified_user_submissions.append(simplified_user_data)

    # Save the simplified posts to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(simplified_user_submissions, file, indent=4)

    print(f"Simplified data saved to {output_file}")
    print(f"Total number of simplified posts: {total_simplified_posts}")

def main():
    parser = argparse.ArgumentParser(description='Simplify user submissions JSON file for NLP projects.')
    parser.add_argument('input_file', type=str, help='Path to the input JSON file containing all user submissions')
    parser.add_argument('output_file', type=str, help='Path to save the simplified JSON file')

    args = parser.parse_args()

    simplify_posts(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
