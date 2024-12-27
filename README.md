# Groninger-Archieven

This repository contains scripts developed for the **Groninger Archieven** project, aimed at processing historical documents to extract valuable information about individuals. The pipeline includes converting PDF files to images, preprocessing these images, performing Optical Character Recognition (OCR), and extracting personal details using a Large Language Model (LLM).

## Table of Contents

- [Project Overview](#project-overview)
- [Pipeline Workflow](#pipeline-workflow)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Project Overview

This project was designed to process old Dutch address books from the **Groninger Archieven**. The pipeline performs the following tasks:

1. Converts multi-page PDF files into PNG images for further processing.
2. Binarizes the PNG images to enhance OCR accuracy.
3. Performs OCR to extract text from the binarized images.
4. Identifies and extracts personal details (e.g., names and addresses) using a Large Language Model.

The ultimate goal is to create a structured dataset of persons mentioned in these historical documents.

---

## Pipeline Workflow

1. **PDF to PNG Conversion**  
   Converts PDF pages into individual PNG files using a script. This ensures compatibility with subsequent image processing tasks.

2. **Image Binarization**  
   Prepares the images for OCR by binarizing them to reduce noise and improve text clarity.

3. **OCR Processing**  
   Uses OCR technology to extract raw text data from the processed images.

4. **Entity Extraction with LLM**  
   Processes the OCR output to identify and extract personal details (names, addresses, etc.) using a Large Language Model.

---

## Repository Structure

groninger-archieven-ocr-pipeline/ ├── scripts/ │ ├── convert_pdf_to_png.py # Converts PDF files to PNG images │ ├── binarize_images.py # Binarizes PNG images │ ├── perform_ocr.py # Performs OCR on the images │ ├── extract_persons_llm.py # Extracts personal details using an LLM ├── data/ │ ├── pdfs/ # Input PDF files │ ├── images/ # Output images (PNG) │ ├── binarized_images/ # Binarized images │ ├── ocr_results/ # OCR output text files │ ├── extracted_persons/ # Extracted data ├── README.md # Project documentation ├── requirements.txt # Required Python libraries └── LICENSE # License information

