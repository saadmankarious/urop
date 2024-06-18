from google.cloud import bigquery

# Initialize a BigQuery client
client = bigquery.Client(project='ramz-b9f9b')

# Define the dataset ID
dataset_id = 'fh-bigquery.reddit_posts'

# List tables in the dataset
tables = client.list_tables(dataset_id)  # Make an API request

print(f"Tables in dataset {dataset_id}:")
for table in tables:
    print(table.table_id)

