import threading
import requests
import os
import csv
import json
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Constants that I am using for this program
API_URL = "https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items"
DATA_DIR = "cms_data"
METADATA_FILE = "last_run_metadata.json"
NUM_WORKERS = 5

# Creating data directory
os.makedirs(DATA_DIR, exist_ok=True)

# Load last run metadata to read
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "r") as f:
        last_run_metadata = json.load(f)
else:
    last_run_metadata = {}

# Convert column names to snake_case
def to_snake_case(name):
    return re.sub(r'[^a-zA-Z0-9]+', '_', name).strip('_').lower()

# Download and process individual CSV
def process_csv(item):
    title = item.get("title", "")
    modified = item.get("modified", "")
    distributions = item.get("distribution", [])
    if not distributions:
        return
    download_url = distributions[0].get("downloadURL", "")

    # check if the title contains "Hospital" 
    if "Hospital" not in title or not download_url.endswith(".csv"):
        return

    # Check if the file has been modified since last run     
    if title in last_run_metadata and last_run_metadata[title] == modified:
        return

    try:
        # Get the current thread name for chekcing parallel run
        thread_name = threading.current_thread().name
        print(f"[{thread_name}] Downloading and processing: {title}")

        # Download the CSV file
        response = requests.get(download_url)
        response.raise_for_status()
        content = response.text

        # Convert the CSV content to snake_case and save it
        filename = os.path.join(DATA_DIR, to_snake_case(title) + ".csv")
        lines = content.splitlines()
        reader = csv.DictReader(lines)
        new_fieldnames = [to_snake_case(field) for field in reader.fieldnames]

        # Write the modified CSV file
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=new_fieldnames)
            writer.writeheader()
            for row in reader:
                writer.writerow({to_snake_case(k): v for k, v in row.items()})

        # Update last run metadata
        last_run_metadata[title] = modified
        print(f" Processed: {title}")

    except Exception as e:
        print(f" Error processing {title}: {e}")

# Main function
def main():
    print(" Fetching CMS dataset metadata...")
    response = requests.get(API_URL)
    response.raise_for_status()
    items = response.json()

    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        executor.map(process_csv, items)

    with open(METADATA_FILE, "w") as f:
        json.dump(last_run_metadata, f, indent=2)
    print(" All done.")

if __name__ == "__main__":
    main()
