import pandas as pd
import requests
import os
import re
import time

# ========== Configuration ==========

# 1. CSV file path (absolute or relative)
csv_file = "ally-786090-Fall_2025_KIN-4250-IO1-2025-06-19-16-01.csv"  # Update the CSV
df = pd.read_csv(csv_file)

# 2. Filter DataFrame: only rows with Mime type == 'application/pdf' and Scanned:1 == 1
df = df[(df['Mime type'] == 'application/pdf') & (df['Scanned:1'] == 1)]
df.info()

# 3. Columns in your CSV containing file info
file_id_column = "Id"
filename_column = "Name"

# 4. Canvas API settings
canvas_token = "0000~ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # <-- Replace with your actual Canvas API token
base_url = "https://usu.instructure.com"

headers = {
    "Authorization": f"Bearer {canvas_token}"
}

# 5. Download folder (change this to any path you want)
output_folder = r"C:\Users\A02424672\Documents\Canvas BulkFlow\Downloads"
os.makedirs(output_folder, exist_ok=True)

# ========== Utility Functions ==========
def sanitize_filename(name: str) -> str:
    """
    Removes characters not allowed on Windows file systems.
    """
    return re.sub(r'[\\/*?:"<>|]', "", name)

# ========== Identify Duplicate Filenames First ==========

# Find all filenames that appear more than once in the CSV
duplicate_filenames_df = df[df.duplicated(subset=[filename_column], keep=False)]
duplicate_names = set(duplicate_filenames_df[filename_column].unique())

# ========== Main Download Logic ==========
def main():
    # We'll keep track of:
    # 1) files that were skipped due to duplication
    # 2) files that were downloaded
    skipped_duplicates = []
    downloaded_files = []

    for index, row in df.iterrows():
        file_id = row[file_id_column]
        file_name = sanitize_filename(str(row[filename_column]))

        # Skip if no file ID
        if pd.isna(file_id):
            print(f"[Row {index}] Missing File ID. Skipping.")
            continue

        # If this file name is in the duplicates set, skip *all* instances
        if file_name in duplicate_names:
            skipped_duplicates.append((file_id, file_name))
            print(f"[Row {index}] Skipping ALL duplicates named '{file_name}' (File ID: {file_id}).")
            continue

        # 1. Fetch file metadata from Canvas API
        file_api_url = f"{base_url}/api/v1/files/{int(file_id)}"
        meta_resp = requests.get(file_api_url, headers=headers)
        if meta_resp.status_code != 200:
            print(f"[Row {index}] Failed to retrieve metadata for file ID {file_id} (Status: {meta_resp.status_code}). Skipping.")
            continue

        file_info = meta_resp.json()
        download_url = file_info.get("url")
        expected_size = file_info.get("size")

        if not download_url:
            print(f"[Row {index}] No download URL found for file ID {file_id}. Skipping.")
            continue

        # 2. Download the file
        print(f"[Row {index}] Downloading {file_name} from {download_url}")
        download_resp = requests.get(download_url, headers=headers, stream=True)
        if download_resp.status_code != 200:
            print(f"[Row {index}] Failed to download {file_name} (Status: {download_resp.status_code}).")
            continue

        # Check the response Content-Type for debugging
        content_type = download_resp.headers.get("Content-Type", "")
        if "application/pdf" not in content_type.lower():
            print(f"[Row {index}] Warning: {file_name} returned unexpected Content-Type: {content_type}")

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
            print(f"[Row {index}] Downloaded {file_name} is smaller than expected "
                  f"(Expected: {expected_size} bytes, Got: {actual_size} bytes).")
        else:
            print(f"[Row {index}] Downloaded {file_name} ({actual_size} bytes) successfully.")

        downloaded_files.append((file_id, file_name))

        # Optional: short pause to reduce chance of rate-limiting
        time.sleep(1)

    # Final summary
    print("\n=== DOWNLOAD SUMMARY ===")
    print(f"Downloaded: {len(downloaded_files)} files.")
    if skipped_duplicates:
        print(f"Skipped {len(skipped_duplicates)} files due to name duplication:")
        for (dup_id, dup_name) in skipped_duplicates:
            print(f"  - File ID: {dup_id}, Name: {dup_name}")
    else:
        print("No duplicates were skipped.")

# ========== Script Entry Point ==========
if __name__ == "__main__":
    main()
