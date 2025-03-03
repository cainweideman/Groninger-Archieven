![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)

# Groninger-Archieven

This repository contains scripts developed for the **Groninger Archieven** project, aimed at processing historical documents to extract valuable information about individuals. The pipeline includes converting PDF files to images, preprocessing these images, performing Optical Character Recognition (OCR), and extracting personal details using a Large Language Model (LLM).

## Table of Contents

- [Project Overview](#project-overview)
- [Pipeline Workflow](#pipeline-workflow)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Serving a LLM on Hábrók](#serving-a-llm-on-hábrók)
  - [Usage](#usage)
- [Repository Structure](#repository-structure)
- [Acknowledgments](#acknowledgments)

## Project Overview

This project was designed to process old Dutch address books from the **Groninger Archieven**. The pipeline performs the following tasks:

1. Converts multi-page PDF files into JPG images for further processing.
2. Binarizes the PNG images to enhance OCR accuracy.
3. Performs OCR to extract text from the binarized images.
4. Identifies and extracts personal details (e.g., names and addresses) using a Large Language Model.
5. Combines the JSON output of the LLM into one JSON per book (optional).
6. Converts the JSON files into CSV files (optional).

The ultimate goal is to create a structured dataset of persons mentioned in these historical documents.

---

## Pipeline Workflow

1. **`convert_jpg_to_png.py`**  
   Converts PDF pages into individual JPG files using a script. This ensures compatibility with subsequent image processing tasks.

2. **`binarize_images.py`**  
   Prepares the images for OCR by binarizing them to reduce noise and improve text clarity.

3. **`ocr.py`**  
   Uses OCR technology to extract raw text data from the processed images.

4. **`extract_people.py`**  
   Processes the OCR output to identify and extract personal details (names, addresses, etc.) using a Large Language Model.

5. **(optional) `combine_jsons.py`**  
   Combines multiple JSON files found in a directory with nested subdirectories into one JSON file per subdirectory.  
   **Note**: Ensure the input directory is structured as follows:
   ```plaintext
   input_folder/
   ├── subdir1/
   │   ├── file1.json
   │   └── file2.json
   ├── subdir2/
   │   ├── file3.json
   │   └── file4.json  

6. **(optional) `convert_json_to_csv.py`**  
   Converts a JSON file into a CSV file.



## Getting Started

### Prerequisites

Before running the scripts in this repository, ensure the following prerequisites are met:

#### 1. Python Environment
- Install **Python 3.11** or later.  
- Ensure you have `pip` installed for managing Python packages.

#### 2. Large Language Model Access
- The `extract_people.py` script utilizes a Large Language Model (e.g., Meta's Llama-3.1-8B-Instruct). Ensure you have:
  - Access to the model's API or framework.
  - Necessary hardware or cloud resources if running the model locally.

##### Set Up Access Token:
1. Request access to the LLM on [Huggingface](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)
2. Create an access token on your Huggingface account and add 'meta-llama/Llama-3.1-8B-Instruct' repo to the repository permissions.
3. Check all write and read options for this access token and save the token.
4. copy and save your access token value.

> **Note:** Refer to your LLM provider's documentation for specific setup instructions.

---

### Installation
#### Step 1: Clone the repository
   ```bash
   git clone https://github.com/cainweideman/Groninger-Archieven.git
   cd Groninger-Archieven
   ```
#### Step 2: Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
#### Step 3: Install Tesseract OCR
#### Windows:
1. **Download Tesseract**:
   - Go to the [Tesseract OCR Installation page](https://github.com/UB-Mannheim/tesseract/wiki).
   - Download the latest stable version for Windows.
   
2. **Run the Installer**:
   - Launch the downloaded `.exe` file to start installation.
   - By default, Tesseract is installed in: C:\Program Files\Tesseract-OCR
   - During installation, select **Dutch (Flemish)** under additional language options.

3. **Add Tesseract OCR to path**:
   1. **Open Environment Variables**:  
      - Press `Win + S` and search for "Environment Variables."  
      - Select **Edit the system environment variables**.  

   2. **Edit PATH Variable**:  
      - In the **System Properties** window, click **Environment Variables**.  
      - Under **System variables**, find the `Path` variable, select it, and click **Edit**.  

   3. **Add Tesseract Path**:  
      - Click **New** and add the path to the Tesseract executable:  
      `C:\Program Files\Tesseract-OCR`  

   4. **Verify the PATH**:  
      - Open a new Command Prompt and type:  
         ```bash
         tesseract --version
         ```  
      - If the version information is displayed, Tesseract is successfully added to your PATH.

4. **Specify the Tesseract Path in Your Script**:
   - Uncomment line 74 in ocr.py and make sure that it refers to where tesseract is installed:
      ```python
      #pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
      ```

#### MacOS:

#### Install Homebrew (if not already installed):
1. Open the Terminal and run:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Follow the on-screen instructions to complete the installation.

#### Verify Homebrew installation:
```bash
brew --version
```

#### Install Tesseract using Homebrew:
```bash
brew install tesseract-lang
```

---

### Serving a LLM on Hábrók:
- Windows: download and use [MobaX](https://mobaxterm.mobatek.net/download-home-edition.html).
- MacOS: use terminal.

#### 1. Login with your account on Hábrók:
- Open a terminal and type the following:
- Use your RUG credentials to login.

```bash
ssh <pnumber>@login1.hb.hpc.rug.nl
```

> **Note:** If login1 does not work, you can try login2.

#### 2. Start an interactive job on an A100 node (single GPU):
- Adjust the time based on the task you will run.

```bash
srun --nodes=1 --ntasks=1 --partition=gpushort --mem=120G --time=04:00:00 --gres=gpu:a100:1 --pty bash
```

#### 3. Load the Python and CUDA modules:
```bash
module load Python/3.11.5-GCCcore-13.2.0 CUDA/12.1.1
```
> **Note:** Only required during the setup.

#### 4. Create a virtual environment:
- Additional information can be found on the [Hábrók-wiki](https://wiki.hpc.rug.nl/habrok/examples/python#building_the_python_virtual_environment)
```bash
python3 -m venv llm
```
> **Note:** Later, you only need to activate it.

#### 5. Activate the virtual environment:
```bash
source llm/bin/activate
```

#### 6. Upgrade pip (optional):
```bash
pip install --upgrade pip
```

#### 7. Install vllm:
```bash
pip install vllm
```
> **Note:** The installation might take some time.

#### 8. Add your Huggingface token to your environment:
```bash
export HF_HOME=/tmp
export HF_TOKEN=<HuggingFace Token>
```
> **Note:** Perform this step everytime you activate the enviroment.

#### 9. Serve the model:
```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct --download-dir /tmp/models --max-model-len 1024 --gpu-memory-utilization 0.95 --port 8000
```
> **Note:** This downnloads the model to the /tmp/model folder.

#### 10. Forward Hábrók port to your local port:
- Use your RUG credentials again.
- Open a second terminal and enter the following:

```bash
ssh -NL 8000:a100gpu6:8000 pnumber@login1.hb.hpc.rug.nl
```

> **Note:** Take note of the node it is running on (e.g. a100gpu6)

#### 11. Verify:
- Open a browser on your device and enter the following address:
```bash
http://localhost:8000/v1/models
```
- You should see the LLM running.

---

### Usage

Each script in this repository uses command-line arguments to configure its behavior. Below is a detailed description of the parameters for each script:

### 1. `convert_pdf_to_jpg.py`
Converts multi-page PDFs into JPG images.

- `--input`: Path to the PDF file.  
- `--output` (optional): Path to save the generated images. If not specified, images are saved in a default directory.

**Example Command:**
```bash
python convert_pdf_to_jpg.py --input 1926.pdf --output image_folder/1926/
```

### 2. `binarize_images.py`
Binarize and crop a single image, directory, or nested directories.

- `--input`: Path to the PDF file or directory.  
- `--output` (optional): Path to the output directory. Default: 'binarized_images' in the current working directory.
- `--threshold` (optional): Threshold value for binarization. Default: 160.
- `--crop` (optional): Fraction of the image dimensions to crop from each side. Default: 0.00

**Example Command:**
```bash
python binarize_images.py --input image_folder/1926/ --output binarized_images/1926/ --threshold 165 --crop 0.05
```

### 3. `ocr.py`
Perform OCR using Tesseract on a single image or a directory of images.

- `--input`: Path to a single image, or a directory of images.
- `--output` (optional): Path to the output directory. Default: 'ocr_results' in the current working directory.
- `--config` (optional): Set the configuration for Tesseract page segmentation modes. Default: 3

```plaintext
Page segmentation modes:
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR.
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
```

**Example Command:**
```bash
python ocr.py --input binarized_images/1926/ --output ocr_results/ --config 4
```

### 4. `extract_people.py`
Processes the OCR output to identify and extract personal details (names, addresses, etc.) using a Large Language Model.
Saves the results in a JSON file per page.

- `--input`: Path to the input file.
- `--output` (optional): Path to the output directory. Default: Name of the input file in the current working directory.
- `--start_page`: First page you want to process.
- `--end_page`: Last page you want to process.

```bash
python extract_people.py --input ocr_results/1926.json --output llm_results/1926 --start_page 121 --end_page 607
```

> **Note:** Ensure the LLM is served before running this script.

### 5. `combine_jsons.py`
Combine the directory of subdirectories containing the LLM results into a single JSON file per subdirectory.

- `--input`: Path to the input directory.
- `--output` (optional): Path to the output directory. Default: 'combined_jsons' in the current working directory.

```bash
python combine_jsons.py --input llm_results/ --output combined_llm_results/
```

### 6. `convert_json_to_csv.py`
Convert a combined JSON into a CSV file.

- `--input`: Path to the input file.
- `--output` (optional): Path to the output file. Default: 'combined_json.csv' in the current working directory.
```bash
python convert_json_to_csv --input combined_llm_results/1926.json --output csv_llm_results/1926.csv
```

---

## Repository Structure

```plaintext
Groninger-Archieven/
├── templates/                   # All templates for prompts, schema's, and dictionaries (required for extract_people.py)
│   ├── json_schema.py           # JSON schema for the output of the LLM
│   ├── page_object.py           # JSON schema for a bookpage
│   ├── prompt.py                # Template for LLM user prompt
|   └── system_message.py        # Template for LLM system prompt
|
├── convert_pdf_to_jpg.py        # Convert PDF to single JPG images
├── binarize_images.py           # Preprocess images for OCR
├── ocr.py                       # Performs OCR on images
├── extract_people.py            # Extract people from OCR data using LLM
├── combine_jsons.py             # Combined JSON files in a directory into one JSON file
├── convert_json_to_csv.py       # Converts a JSON file into a CSV file
|
├── README.md                    # Project documentation and instructions
├── requirements.txt             # List of required Python libraries
└── .gitignore                   # Files and directories to ignore in Git
```
---

## Acknowledgments

This project was developed in collaboration with [**Groninger Archieven**](https://www.groningerarchieven.nl/), which provided access to their historical address books for analysis. We would like to thank the project team, including Emin Tatar, Lieuwe Jongsma, Kick Bartram, Nathan Peitz, Timucin Mutlu, Minxuan Wang, Viktor Alarov, and Cain Weideman, for their dedication and contributions.

We utilized [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for text recognition, Meta's [Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) model for extracting personal details from the processed text, and the High Performance Computing Cluster [Hábrók](https://www.rug.nl/society-business/center-for-information-technology/research/services/hpc/habrok) from Rijksuniversiteit Groningen to run the Llama model. We extend our gratitude to the developers and maintainers of these powerful tools, whose contributions made this project possible.
