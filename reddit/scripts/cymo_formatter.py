import json
import csv
import argparse

def convert_json_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the header
        csv_writer.writerow(['TID', 'text'])

        for user_data in data:
            username = user_data['username']
            for post in user_data['posts']:
                tid = f"{username}_{post['id']}"
                text = post.get('selftext', '')
                csv_writer.writerow([tid, text])

    print(f"Data has been successfully converted to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Convert JSON file to CSV with specified format.')
    parser.add_argument('input_file', type=str, help='Path to the input JSON file')
    parser.add_argument('output_file', type=str, default='output.cymo.csv', help='Path to save the output CSV file')

    args = parser.parse_args()

    convert_json_to_csv(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
