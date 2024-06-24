import json
import csv
import argparse

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def format_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['TID', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in data:
            diagnosed_user = entry['diagnosed_user']
            controls = entry['controls']
            for control in controls:
                control_user = control['username']
                posts = control['posts']
                for post in posts:
                    tid = f"{post['subreddit']}_{diagnosed_user}_{control_user}_{post['id']}"
                    text = post['selftext']
                    writer.writerow({'TID': tid, 'text': text})

def main():
    parser = argparse.ArgumentParser(description='Format JSON data to CSV.')
    parser.add_argument('input_file', type=str, help='Path to the input JSON file')
    parser.add_argument('output_file', type=str, help='Path to the output CSV file')

    args = parser.parse_args()

    data = load_json(args.input_file)
    format_to_csv(data, args.output_file)

if __name__ == '__main__':
    main()
