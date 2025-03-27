# Canvas BulkFlow

**Canvas BulkFlow** is a two-step solution for batch-downloading PDF files from Canvas, running them through OCR (via a third-party tool), and then batch-uploading the newly OCRed files back to Canvas.

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Workflow Diagram](#workflow-diagram)  
7. [FAQ & Troubleshooting](#faq--troubleshooting)  
8. [Contributing](#contributing)  
9. [License](#license)

---

## Overview

Many institutions use Canvas for course content management. However, PDFs in Canvas might be non-OCRed (i.e., not searchable). **Canvas BulkFlow** automates:

1. **Bulk Download**: Pulling non-OCRed PDFs from Canvas (identified via an Ally report or another listing).  
2. **OCR Conversion**: Converting the downloaded files into OCRed PDFs using third-party software (e.g., ABBYY FineReader).  
3. **Bulk Upload**: Replacing the original files in Canvas with their new, searchable PDF versions.

This workflow improves document accessibility and ensures students can search within course materials more easily.

---

## Features

- **Batch Handling**: Download and upload large collections of PDFs with a single script execution.  
- **Canvas API Integration**: Uses [`canvasapi`](https://github.com/ucfopen/canvasapi) to interact with Canvas LMS.  
- **Ally-Report Based**: Reads an Ally report (or a similar CSV) to identify file IDs and names.  
- **Modular Notebooks**: Two Jupyter notebooks (or Python scripts) for clear separation of tasks.

---

## Prerequisites

1. **Canvas API Credentials**  
   - You need a valid API token (Canvas Access Token) from your Canvas LMS.  
   - Set the environment variable or store it in a config file for secure usage.

2. **Ally Report (or equivalent CSV)**  
   - A CSV or similar file listing the Canvas file IDs, filenames, etc.  
   - Adjust the code if your CSV format differs from the default Ally format.

3. **Python 3.7+**  
   - Make sure you’re running a recent version of Python to match the libraries used.

4. **Python Libraries**  
   - [`canvasapi`](https://pypi.org/project/canvasapi/)  
   - `requests`  
   - Any other libraries mentioned in your `requirements.txt` or notebooks.

5. **OCR Software** (e.g., ABBYY FineReader)  
   - Not directly included in this repo.  
   - Configure your OCR solution to watch a “Hot Folder” or follow the process you use for batch OCR.

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/YOUR_USERNAME/Canvas-BulkFlow.git
   cd Canvas-BulkFlow

   
2. **Create and Activate a Virtual Environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux

   ## Or

   venv\Scripts\activate      # On Windows

3. **Install Required Dependencies**
   ```bash
   pip install -r requirements.txt

   
4. **Configure Your Canvas API Key**
   ```bash
   CANVAS_API_URL = "https://<YOUR_CANVAS_DOMAIN>/api/v1"
   CANVAS_API_KEY = "<YOUR_CANVAS_API_TOKEN>"


## Usage

The solution is split into two main notebooks:

1. **`Canvas_Bulk_Download.ipynb`**  
   - **Purpose**: Downloads all non-OCRed files.  
   - **How to run**:  
     1. Open the notebook in VS Code or Jupyter Lab.  
     2. Update the file paths and Canvas credentials.  
     3. Run all cells.  
   - **Output**: A local folder containing downloaded PDFs.

2. **Process your PDFs through OCR (done externally)**  
   - Using **ABBYY FineReader** or another OCR tool, convert the downloaded PDFs to searchable PDFs.

3. **`Canvas_Bulk_Upload.ipynb`**  
   - **Purpose**: Uploads the newly OCRed PDFs back to Canvas, replacing the original versions.  
   - **How to run**:  
     1. Ensure your OCRed PDFs are in the correct folder.  
     2. Update the file paths (and if needed, the CSV references).  
     3. Run the notebook.  
   - **Output**: Canvas courses/files are updated with the new OCRed PDFs.

## Workflow Diagram
```rust
Ally Report CSV  -->  Canvas_Bulk_Download.ipynb  -->  Local Folder

Local Folder   -->  OCR Software (Hot Folder)   -->  OCRed PDFs

OCRed PDFs     -->  Canvas_Bulk_Upload.ipynb    -->  Canvas Files Updated
```

## FAQ & Troubleshooting

**My files aren’t downloading.**  
- Check your API token and Canvas domain. Make sure they are correct.  
- Double-check the Ally report CSV columns are named correctly in the script.

**I get `ModuleNotFoundError` when running notebooks.**  
- Confirm you’ve installed all dependencies in your current environment.  
- Use the same interpreter in VS Code that has your packages installed.

**OCRed files aren’t being updated in Canvas.**  
- Ensure the file IDs match those in the Ally report.  
- Make sure the script is pointing to the correct folder of OCRed PDFs.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you find bugs or want to improve this workflow.

## License

**MIT License** – You are free to modify and distribute this project. See `LICENSE` for details.
