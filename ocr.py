import os
import json
import argparse
import pytesseract
from PIL import Image
from tqdm import tqdm


def ocr_page(input_path, language="nld", config=3):
    try:
        image = Image.open(input_path)
        configuration = "--psm " + str(config)
        text = pytesseract.image_to_string(image, lang=language, config=configuration)
        return text
    except FileNotFoundError:
        print(f"Error: File not found - {input_path}")
        return ""
    except Exception as e:
        print(f"Error processing file {input_path}: {e}")
        return ""


def process_directory(input_path, output_dir, language="nld", config=3):
    try:
        if not os.path.exists(input_path):
            print(f"Error: Input directory does not exist - {input_path}")
            return

        file_name = os.path.splitext(os.path.basename(input_path))[0]
        data = {
            "year": file_name,
            "content": []
        }

        files = [file for file in os.listdir(input_path) if file.lower().endswith(".jpg")]

        if not files:
            print(f"Warning: No image files found in {input_path}")
            return

        for page_number, file in tqdm(enumerate(files), total=len(files), ncols=100, desc="OCRing Images", unit="image"):
            img_path = os.path.join(input_path, file)
            try:
                text = ocr_page(img_path, language, config)
                if text.strip():
                    page_data = {
                        "page": page_number + 1,
                        "text": text
                    }
                    data["content"].append(page_data)
            except Exception as e:
                print(f"Error processing image {img_path}: {e}")

        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except OSError as e:
                print(f"Error: Failed to create output directory - {output_dir}. {e}")
                return

        output_path = os.path.join(output_dir, file_name + ".json")
        try:
            with open(output_path, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4)
            print(f"Successfully saved OCR results to {output_path}")
        except IOError as e:
            print(f"Error: Failed to save JSON file - {output_path}. {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    parser = argparse.ArgumentParser(description="Convert PDF files to JPG images.")
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to a single image, or a directory of images.")
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory. Default: 'ocr_results' in the current working directory.", default="./ocr_results")
    parser.add_argument("-c", "--config", type=int, help="Set the configuration for Tesseract.", default=3)

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
        ocr_page(img_path=input_path, language=args.langauge, config=args.config)
    elif os.path.isdir(input_path):
        # Directory or nested directories of PDFs
        print(f"Processing directory: {input_path}")
        process_directory(img_path=input_path, output_dir=output_dir, language=args.langauge, config=args.config)
    else:
        print(f"Error: The input path {input_path} does not exist or is not valid.")
        exit(1)

if __name__ == "__main__":
    main()