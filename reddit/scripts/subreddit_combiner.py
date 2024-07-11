import os
import json
import argparse

def process_file(filepath, authors_data):
    with open(filepath, 'r') as file:
        for line in file:
            data = json.loads(line)
            author = data.get('author')
            if author:
                if author not in authors_data:
                    authors_data[author] = {'comments': [], 'posts': []}
                if 'body' in data:
                    authors_data[author]['comments'].append(data)
                elif 'title' in data:
                    authors_data[author]['posts'].append(data)

def save_combined_data(authors_data, comments_output_file, posts_output_file):
    with open(comments_output_file, 'w') as comments_file, open(posts_output_file, 'w') as posts_file:
        for author, content in authors_data.items():
            for comment in content['comments']:
                comments_file.write(json.dumps(comment) + '\n')
            for post in content['posts']:
                posts_file.write(json.dumps(post) + '\n')

def main(input_directory, comments_output_file, posts_output_file):
    authors_data = {}
    for root, _, files in os.walk(input_directory):
        for file in files:
            print(f'read file {file}')
            if file.endswith("_comments.jsonl") or file.endswith("_posts.jsonl"):
                process_file(os.path.join(root, file), authors_data)
    save_combined_data(authors_data, comments_output_file, posts_output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine JSONL files into single comments and posts files grouped by author.')
    parser.add_argument('input_directory', type=str, help='Path to the input directory containing the JSONL files')
    args = parser.parse_args()

    input_directory = args.input_directory
    comments_output_file = args.input_directory + '/combined_comments.jsonl'
    posts_output_file =  args.input_directory + '/combined_posts.jsonl'
    
    main(input_directory, comments_output_file, posts_output_file)
