import pandas as pd
import requests
import os
import re
import time

# ========== Configuration ==========

# 1. CSV file path (absolute or relative)
csv_file = "YourExcelFile.csv"
df = pd.read_csv(csv_file)

# 2. Filter DataFrame: only rows with Mime type == 'application/pdf' and Ocred:2 == 0
df = df[(df['Mime type'] == 'application/pdf') & (df['Ocred:2'] == 0)]
df.info()

# 3. Columns in your CSV containing file info
file_id_column = "Id"
filename_column = "Name"

# 4. Canvas API settings
canvas_token = "1234~ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # <-- Replace with your actual Canvas API token
base_url = "https://usu.instructure.com"

headers = {
    "Authorization": f"Bearer {canvas_token}"
}

# 5. Download folder (change this to any path you want)
output_folder = r"C:\Users\Your_A-Number\Documents\Canvas BulkFlow\Downloads"
os.makedirs(output_folder, exist_ok=True)

# ========== Utility Functions ==========

def sanitize_filename(name: str) -> str:
    """
    Removes characters not allowed on Windows file systems.
    """
    return re.sub(r'[\\/*?:"<>|]', "", name)

# ========== Main Download Logic ==========

def main():
    # Loop through each row in the filtered DataFrame
    for index, row in df.iterrows():
        file_id = row[file_id_column]
        file_name = sanitize_filename(str(row[filename_column]))

        # Skip if no file ID
        if pd.isna(file_id):
            print(f"Row {index} has no File ID. Skipping.")
            continue

        # 1. Fetch file metadata from Canvas API
        file_api_url = f"{base_url}/api/v1/files/{int(file_id)}"
        meta_resp = requests.get(file_api_url, headers=headers)

        if meta_resp.status_code != 200:
            print(f"Failed to retrieve metadata for file ID {file_id} "
                  f"(Status: {meta_resp.status_code}). Skipping.")
            continue

        file_info = meta_resp.json()
        download_url = file_info.get("url")
        expected_size = file_info.get("size")

        if not download_url:
            print(f"No download URL found for file ID {file_id}. Skipping.")
            continue

        # 2. Download the file
        print(f"Downloading {file_name} from {download_url}")
        download_resp = requests.get(download_url, headers=headers, stream=True)

        if download_resp.status_code != 200:
            print(f"Failed to download {file_name} (Status: {download_resp.status_code}).")
            continue

        # Check the response Content-Type for debugging
        content_type = download_resp.headers.get("Content-Type", "")
        if "application/pdf" not in content_type.lower():
            print(f"Warning: {file_name} returned unexpected Content-Type: {content_type}")

        # 3. Save the file to disk
        filepath = os.path.join(output_folder, file_name)
        with open(filepath, "wb") as f:
            for chunk in download_resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        download_resp.close()

        # 4. Verify file size
        actual_size = os.path.getsize(filepath)
        if expected_size and actual_size < expected_size:
            print(f"Downloaded {file_name} is smaller than expected "
                  f"(Expected: {expected_size} bytes, Got: {actual_size} bytes).")
        else:
            print(f"Downloaded: {file_name} ({actual_size} bytes) successfully.")

        # Optional: short pause to reduce chance of rate-limiting
        time.sleep(1)

    print("All downloads complete!")

# ========== Script Entry Point ==========
if __name__ == "__main__":
    main()
