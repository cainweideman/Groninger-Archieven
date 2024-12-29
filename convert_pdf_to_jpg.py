import os
import fitz
import argparse
from tqdm import tqdm

def convert_pdf_to_jpg(input_path, output_dir, zoom=2, dpi=200):
    try:
        # Open the PDF file
        doc = fitz.open(input_path)
        total_pages = doc.page_count
    except fitz.fitz.FileDataError:
        print(f"Error: '{input_path}' is not a valid PDF file or is corrupted.")
    except Exception as e:
        print(f"An unexpected error occurred while opening '{input_path}': {e}")
    
    for page_number in tqdm(range(len(total_pages)), desc='Converting pages', ncol=100, unit='page'):
        page = doc.load_page(page_number)
        mat = fitz.Matrix(zoom, zoom)  # Scale matrix for high resolution
        image = page.get_pixmap(matrix=mat, dpi=dpi)
        
        # Construct output filename with zero-padded page number
        output_filename = f"{os.path.basename(input_path).split('.')[0]}_page_{page_number:04}.jpg"
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            image.save(output_path, format="JPEG")
        except PermissionError:
            print(f"Error: Permission denied when saving to '{output_path}'.")
        except FileNotFoundError:
            print(f"Error: Directory does not exist for '{output_path}'.")
        except OSError as e:
            print(f"Error: An OS error occurred while saving to '{output_path}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred while saving to '{output_path}': {e}")
    
    doc.close()


def process_directory(input_path, output_dir):
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                convert_pdf_to_jpg(pdf_path, output_dir)


def main():
    parser = argparse.ArgumentParser(description="Convert PDF files to JPG images.")
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to a single PDF, a directory of PDFs, or a directory containing nested directories with PDFs.")
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory. Default: 'output' in the current working directory.", default="./output",)

    args = parser.parse_args()

    # Access the arguments
    input_path = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            print(f"Failed to create directory: {e}")

    if os.path.isfile(input_path):
        # Single PDF file
        print(f"Processing single file: {input_path}")
        convert_pdf_to_jpg(input_path, output_dir)
    elif os.path.isdir(input_path):
        # Directory or nested directories of PDFs
        print(f"Processing directory: {input_path}")
        process_directory(input_path, output_dir)
    else:
        print(f"Error: The input path {input_path} does not exist or is not valid.")
        exit(1)

if __name__ == "__main__":
    main()