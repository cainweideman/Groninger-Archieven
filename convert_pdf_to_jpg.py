"""
PDF to Image Conversion Script

This script processes PDF files stored within a specified directory structure. For each PDF:
- Each page is converted to a high-resolution image.
- Images are saved in an 'images' subfolder within each directory.

Modules:
    - fitz (PyMuPDF): For reading and rendering PDF pages as images.
    - os: For directory and file handling.

Functions:
    - create_output_directory: Ensures the output directory for images exists.
    - convert_pdf_to_images: Converts each page of a PDF into an image.
    - process_pdfs_in_directory: Main function that processes PDFs in a directory structure.

Example:
    To use this script, organize your PDFs in a folder with subdirectories for each PDF:
    data/
        ├── folder1/
        │   └── document1.pdf
        ├── folder2/
        │   └── document2.pdf

    The output will be:
    data/
        ├── folder1/
        │   ├── document1.pdf
        │   └── images/
        │       └── document1_page_0000.jpg
        ├── folder2/
        │   ├── document2.pdf
        │   └── images/
        │       └── document2_page_0000.jpg
"""

import fitz  # PyMuPDF
import os

def create_output_directory(path):
    """
    Creates the output directory if it doesn't already exist.

    Parameters:
        path (str): Path to the directory to be created.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def convert_pdf_to_images(pdf_path, output_directory, zoom=2, dpi=200):
    """
    Converts each page of a PDF file to a high-resolution image and saves it.

    Parameters:
        pdf_path (str): Path to the PDF file.
        output_directory (str): Path to the directory where images will be saved.
        zoom (float): Zoom factor for scaling the image resolution.
        dpi (int): Dots per inch for the output images.
    
    Returns:
        None
    """
    doc = fitz.open(pdf_path)
    
    for i in range(len(doc)):
        page = doc.load_page(i)
        mat = fitz.Matrix(zoom, zoom)  # Scale matrix for high resolution
        image = page.get_pixmap(matrix=mat, dpi=dpi)
        
        # Construct output filename with zero-padded page number
        output_filename = f"{os.path.basename(pdf_path).split('.')[0]}_page_{i:04}.jpg"
        output_path = os.path.join(output_directory, output_filename)
        
        image.save(output_path)
    
    doc.close()


def process_pdfs_in_directory(root_directory='data'):
    """
    Processes all PDF files within subdirectories of the specified root directory.
    - Each PDF is converted to images, one per page.
    - Images are saved in an 'images' subfolder within each directory.

    Parameters:
        root_directory (str): Path to the root directory containing PDF subdirectories.
    
    Directory Structure:
        root_directory/
            ├── subdirectory1/
            │   ├── pdf_file1.pdf
            │   └── images/
            │       └── pdf_file1_page_0000.jpg
            ├── subdirectory2/
            │   ├── pdf_file2.pdf
            │   └── images/
            │       └── pdf_file2_page_0000.jpg
    """
    for directory in os.listdir(root_directory):
        dir_path = os.path.join(root_directory, directory)
        
        if not os.path.isdir(dir_path):
            continue  # Skip files in root directory
        
        # Assuming there is only one PDF per subdirectory
        filenames = [f for f in os.listdir(dir_path) if f.endswith('.pdf')]
        if not filenames:
            print(f"No PDF files found in {dir_path}.")
            continue
        
        pdf_path = os.path.join(dir_path, filenames[0])  # Process the first PDF file found
        
        output_directory = os.path.join(dir_path, 'images')
        create_output_directory(output_directory)
        
        print(f"Processing {pdf_path}...")
        convert_pdf_to_images(pdf_path, output_directory)
        print(f"Images saved to {output_directory}")


# Convert the PDF files in every directory
# process_pdfs_in_directory()

# Convert specific PDF file
path_to_pdf = "data/1854/1854.pdf"
output_directory = "data/1854/images"
convert_pdf_to_images(path_to_pdf, output_directory)
