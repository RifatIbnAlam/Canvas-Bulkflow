# Canvas BulkFlow

A Python-based workflow to **bulk download** non-OCR’d PDF files from Canvas, run them through an OCR process, and then **bulk upload** (replace) those PDFs in Canvas with their OCRed versions.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
  - [1. Bulk Download](#1-bulk-download)
  - [2. OCR the Files](#2-ocr-the-files)
  - [3. Bulk Upload](#3-bulk-upload)
- [Configuration](#configuration)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Many Canvas courses contain PDFs that are not accessible (i.e., not OCRed). Manually downloading, OCRing, and re-uploading them is time-consuming. **Canvas BulkFlow** automates this process:

1. **Download** all non-OCRed PDFs from a Canvas course (or multiple courses).
2. **Run an OCR tool** (like ABBYY FineReader) on the downloaded PDFs.
3. **Upload** (replace) the PDFs on Canvas with their newly OCRed versions.

---

## Features

- **Bulk Download**: Fetch multiple PDF files from Canvas using their file IDs.
- **Bulk Upload (Replace)**: Overwrite existing Canvas PDFs with the newly OCRed files.
- **Uses CSV**: Reads file IDs, filenames, and other metadata from a CSV file (generated from an Ally report or other sources).
- **Simple Python Scripts**: No heavy dependencies beyond `requests` and `pandas`.

---

## Prerequisites

1. **Python 3.8+**  
   - Download and install from [python.org](https://www.python.org/downloads/).  
   - Ensure it’s on your system PATH.

2. **Git** (optional but recommended)  
   - For version control. Download from [git-scm.com](https://git-scm.com/).

3. **Canvas API Token**  
   - Generate a personal access token in your Canvas account settings.  
   - Keep it **private**. Don’t commit it to a public repository.

4. **CSV File from Ally Report**  
   - A CSV (e.g., from an Ally report) containing at least:
     - `Id` (Canvas File ID)
     - `Name` (Filename)
     - `Mime type` (Optional but used for filtering)
     - `Ocred:2` or similar column for identifying non-OCRed files

5. **OCR Software**  
   - Example: ABBYY FineReader (or any tool that can process PDFs in bulk).

---

## Setup

1. **Clone or Download this Repo**  
   ```bash
   git clone https://github.com/RifatIbnAlam/Canvas-Bulkflow.git
   cd Canvas-Bulkflow
   
2. **Create and Activate a Virtual Environment (recommended)**
   ```bash
   # Activate it:

   # On Windows:
   .\venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate


3. **Install Required Dependencies**
   ```bash
   pip install requests pandas

   
4. **Configure Your Canvas API Key**
   ```bash
   # Open each script (canvas_bulk_download.py, canvas_bulk_upload.py) and update canvas_token with your actual Canvas token

## Usage

### 1. Bulk Download

#### Prepare CSV
Ensure your CSV includes columns like **Id**, **Name**, **Mime type**, **Ocred:2** (or whichever columns you need).  
Example: `YourExcelFile.csv`

#### Edit `canvas_bulk_download.py`
- Update the `csv_file` path to point to your CSV.
- Update the `output_folder` to where you want PDFs saved.

#### Run the Script
   ```bash
   python canvas_bulk_download.py
   ```

### 2. OCR the Files

Use your chosen OCR tool (e.g., ABBYY FineReader) to convert the downloaded PDFs in bulk.  
By default, you might place the OCRed files into a folder such as `Downloads/OCRed/`.

---

### 3. Bulk Upload

#### Edit `canvas_bulk_upload.py`
- Update the `csv_file` path to point to the same or a merged CSV with the correct columns.
- Update `ocr_folder` (or the logic that builds the local file path) to match where your OCRed PDFs are located.
- Confirm the correct column names (e.g., **Id** for file ID, **Name** for the local filename).

#### Run the Script
   ```bash
   python canvas_bulk_upload.py
   ```
This replaces the existing files in Canvas with the OCRed versions.

---

## Configuration

- **Canvas Token:**  
  Hardcode in the script or load from environment variables.
- **Base URL:**  
  Currently set to `https://usu.instructure.com`. Change if your Canvas instance has a different domain.
- **CSV Columns:**  
  Adjust the scripts if your CSV columns differ (for example, if you have `File_ID` instead of `Id`).

---

## FAQ

**What if I have multiple courses?**  
You can merge multiple CSVs (one per course) into a single CSV as long as each file’s ID is unique. The ID is globally unique across Canvas, so the script will handle each file accordingly. Make sure your local OCRed filenames don’t collide if two different courses have the same “Name.”

**Do I need to worry about duplicate filenames (like `Syllabus.pdf`)?**  
Canvas identifies files by their file ID, not by the filename. However, locally, you might want to rename your OCRed files or organize them into subfolders to avoid overwriting files.

**Why do I get a PermissionError on Windows?**  
Ensure the folder path is valid and you have permission to write/read in that directory. Avoid placing your scripts or data in restricted system folders.

**Why am I getting 401 or 403 errors?**  
Make sure your Canvas token is valid and has the correct permissions. Double-check the base URL for your Canvas instance.

---

## Contributing

1. **Fork** this repository.
2. **Create a feature branch** by typing: `git checkout -b my-feature`
3. **Commit your changes** by typing: `git commit -m 'Add some feature'`
4. **Push to the branch** by typing: `git push origin my-feature`
5. **Open a Pull Request** on GitHub.

---

## License

This project is available under the **MIT License**. Feel free to modify and distribute as needed.
