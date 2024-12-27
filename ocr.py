"""
OCR Processing Script

This script processes images within a specified directory, performing OCR (Optical Character Recognition) on each image.
- The extracted text is saved in a structured JSON file with page numbers and text content.

Modules:
    - pytesseract: For performing OCR on images.
    - PIL.Image: For opening and processing image files.
    - os: For directory and file handling.
    - json: For storing extracted text in JSON format.

Functions:
    - ocr_page: Performs OCR on a single image and returns the text.
    - ocr_directory: Performs OCR on all images within a directory, saving results to a JSON file.

Requires:
    - Tesseract OCR installed and configured (path set in pytesseract.pytesseract.tesseract_cmd).
"""


import pytesseract
from PIL import Image
import os
import json
from tqdm import tqdm

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def ocr_page(path_to_image, language="nld", config="3"):
	"""
	Performs OCR on a single image and returns the extracted text.

	Parameters:
	path_to_image (str): Path to the image file.
	language (str): Language code for OCR (default is Dutch "nld").

	Returns:
	str: Extracted text from the image.
	"""
	image = Image.open(path_to_image)
	configuration = "--psm " + config
	text = pytesseract.image_to_string(image, lang=language, config=configuration)
	return text

def ocr_directory(path_to_images_directory, output_directory, language="nld", config="3"):
	"""
	Performs OCR on all images within a specified directory, storing results in a JSON file.

	Parameters:
	path_to_images_directory (str): Directory path containing image files for OCR.
	output_directory (str): Directory path for saving the output JSON file.
	language (str): Language code for OCR (default is Dutch "nld").

	Output JSON:
	{
		"year": (int),
		"content": [
			{
				"page": (int),
				"text": (str)
			},
			{
				"page": (int),
				"text": (str)
			}
		]
	}

	Example:
    directory/
        ├── path_to_images_directory/
        │   └── image1.jpg

    The output will be:
    directory/
        ├── path_to_images_directory/
        │   └── image1.jpg
        ├── text/
        │   └── directory_text.json
	"""
	book_year = path_to_images_directory.split('/')[1]
	print(f'Performing OCR for {path_to_images_directory}')
	data = {
		"year": book_year,
		"content": []
	}

	content = []

	for page_number, filename in tqdm(enumerate(os.listdir(path_to_images_directory)), total=len(os.listdir(path_to_images_directory)), ncols=100, desc="OCRing Images", unit="image"):
		path_to_image = os.path.join(path_to_images_directory, filename)
		text = ocr_page(path_to_image, language, config)
		page_data = {
			"page": page_number + 1,
			"text": text
		}
		content.append(page_data)
	
	data["content"] = content
	json_string = json.dumps(data, indent=4)

	output_directory_text = os.path.join(output_directory, 'text')
	os.makedirs(output_directory_text, exist_ok=True)
	output_filename = book_year + ".json"
	output_file_path = os.path.join(output_directory_text, output_filename)
	outfile = open(output_file_path, 'a+')
	outfile.write(json_string + '\n')
	outfile.close()

# Set the configuration for Tesseract
'''
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
'''
config = "3"

# OCR a specific page and print the text
path_to_image = "data/1911/images_improved/improved_1911_page_0106.jpg"
#print(ocr_page(path_to_image, config=config))

# OCR all images in a directory
path_to_images_directory = "data/1922/images_improved"
output_directory = "data/1922"
ocr_directory(path_to_images_directory, output_directory, config=config)