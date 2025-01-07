# Groninger-Archieven

This repository contains scripts developed for the **Groninger Archieven** project, aimed at processing historical documents to extract valuable information about individuals. The pipeline includes converting PDF files to images, preprocessing these images, performing Optical Character Recognition (OCR), and extracting personal details using a Large Language Model (LLM).

## Table of Contents

- [Project Overview](#project-overview)
- [Pipeline Workflow](#pipeline-workflow)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [Repository Structure](#repository-structure)
- [Acknowledgments](#acknowledgments)

## Project Overview

This project was designed to process old Dutch address books from the **Groninger Archieven**. The pipeline performs the following tasks:

1. Converts multi-page PDF files into JPG images for further processing.
2. Binarizes the PNG images to enhance OCR accuracy.
3. Performs OCR to extract text from the binarized images.
4. Identifies and extracts personal details (e.g., names and addresses) using a Large Language Model.

The ultimate goal is to create a structured dataset of persons mentioned in these historical documents.

---

## Pipeline Workflow

1. **PDF to PNG Conversion**  
   Converts PDF pages into individual JPG files using a script. This ensures compatibility with subsequent image processing tasks.

2. **Image Binarization**  
   Prepares the images for OCR by binarizing them to reduce noise and improve text clarity.

3. **OCR Processing**  
   Uses OCR technology to extract raw text data from the processed images.

4. **Entity Extraction with LLM**  
   Processes the OCR output to identify and extract personal details (names, addresses, etc.) using a Large Language Model.

---

## Getting Started

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

#### MacOS:
```bash
brew install tesseract-lang
```
### Usage
1. **Convert PDFs to images:**
   ```bash
   python convert_pdf_to_jpg.py --input 1926.pdf [--ouput output/1926]
   ```
2. **Preprocess images:**
   ```bash
   python binarize_images.py --input output/1926 [--output binarized_images/1926]
   ```
3. **Perform OCR:**
   ```bash
   python ocr.py --input binarized_images/1926 [--output ocr_results] [--congif 3]
   ```
4. **Extract people:**
   ```bash
   python extract_people.py --input 1854.json [--output output_folder/1854] --start_page 7 --end_page 209
   ```

---

## Repository Structure

```plaintext
Groninger-Archieven/
├── templates/                   # All templates for prompts, schema's, and dictionaries
│   ├── json_schema.py           # JSON schema for the output of the LLM
│   ├── page_object.py           # JSON schema for a bookpage
│   ├── prompt.py                # Template for LLM user prompt
|   └── system_message.py        # Template for LLM system prompt
|
├── binarize_images.py           # Preprocess images for OCR
├── convert_pdf_to_jpg.py        # Convert PDF to single JPG images
├── extract_people.py            # Extract people from OCR data using LLM
├── ocr.py                       # Performs OCR on images
|
├── README.md                    # Project documentation and instructions
├── requirements.txt             # List of required Python libraries
└── .gitignore                   # Files and directories to ignore in Git
```
---

## Acknowledgments

This project was developed in collaboration with **Groninger Archieven**, which provided access to their historical address books for analysis. We would like to thank the project team, including Emin Tatar, Lieuwe Jongsma, Kick Bartram, Nathan Peitz, Timucin Mutlu, Minxuan Wang, Viktor Alarov, and Cain Weideman, for their dedication and contributions.

We utilized Tesseract OCR for text recognition and a LLaMA model for extracting personal details from the processed text. We extend our gratitude to the developers and maintainers of these powerful tools, whose open-source contributions made this project possible.
