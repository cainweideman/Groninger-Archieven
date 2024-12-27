"""
Image Processing Script

This script processes images stored within a specified directory structure. Each image is:
- Converted to grayscale
- Binarized (converted to black and white)
- Cropped to remove a small margin from each edge
- Saved in a subfolder within each directory.

Modules:
    - cv2: For image reading, processing, and saving.
    - os: For directory and file handling.

Functions:
    - display_image: Display an image with matplotlib.
    - grayscale: Convert an image to grayscale.
    - binarize_image: Apply binary thresholding to a grayscale image.
    - crop_image: Crop a specified margin from the image edges.
    - process_images_in_directory: Main function that processes images in a directory structure.
    - process_image: Function that processes one specific image
    - process_directory: Function that processes the images in a specific directory
"""

import cv2
import os
from tqdm import tqdm

def grayscale(image):
    """
    Converts an image to grayscale.

    Parameters:
        image (numpy.ndarray): Input image in BGR format.

    Returns:
        numpy.ndarray: Grayscale image.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def binarize_image(gray_image, threshold=160, max_value=230):
    """
    Applies binary thresholding to a grayscale image.

    Parameters:
        gray_image (numpy.ndarray): Grayscale image.
        threshold (int): Threshold value for binarization.
        max_value (int): Maximum pixel value to use with the THRESH_BINARY thresholding.

    Returns:
        numpy.ndarray: Binarized (black-and-white) image.
    """
    _, binary_image = cv2.threshold(gray_image, threshold, max_value, cv2.THRESH_BINARY)
    return binary_image


def crop_image(image, crop_fraction=0.05):
    """
    Crops an image by removing a certain fraction from each edge.

    Parameters:
        image (numpy.ndarray): Input image to be cropped.
        crop_fraction (float): Fraction of the image dimensions to crop from each side.

    Returns:
        numpy.ndarray: Cropped image.
    """
    height, width = image.shape[:2]
    top, bottom = int(height * crop_fraction), int(height * (1 - crop_fraction))
    left, right = int(width * crop_fraction), int(width * (1 - crop_fraction))
    return image[top:bottom, left:right]


def process_images_in_directory(root_directory, threshold=160, crop_fraction=0):
    """
    Processes images in a specified directory structure:
    - Converts each image to grayscale
    - Applies binary thresholding
    - Crops the image
    - Saves the processed images in an 'images_improved' subfolder

    Parameters:
        root_directory (str): Path to the root directory containing subdirectories with images.
        threshold (int): Threshold value for binarization.
        crop_fraction (float): Fraction of the image dimensions to crop from each side.
    
    Directory Structure:
        root_directory/
            ├── subdirectory1/
            │   ├── images/
			|	|	└──image1.jpg
            │   └── images_improved/
            │       └── improved_image1.jpg
            ├── subdirectory2/
            │   ├── images/
			|	|	└──image2.jpg
            │   └── images_improved/
            │       └── improved_image2.jpg
    """
    for directory in os.listdir(root_directory):
        path = os.path.join(root_directory, directory)
        if not os.path.isdir(path):
            continue

        filenames = os.listdir(path)
        file_path = os.path.join(path, filenames[-2])

        output_directory = os.path.join(path, 'images_improved')
        os.makedirs(output_directory, exist_ok=True)

        for image_name in os.listdir(file_path):
            image_path = os.path.join(file_path, image_name)
            img = cv2.imread(image_path)

            if img is None:
                print(f"Warning: Unable to read {image_path}")
                continue

            gray_image = grayscale(img)
            binary_image = binarize_image(gray_image, threshold)
            cropped_img = crop_image(binary_image, crop_fraction)

            output_file_path = os.path.join(output_directory, f"improved_{image_name}")
            cv2.imwrite(output_file_path, cropped_img)
            print(f"Processed and saved: {output_file_path}")


def process_image(path_to_image, threshold=160, crop_fraction=0):
	"""
	Processes an image for a specific path:
	- Converts image to grayscale
	- Applies binary thresholding
	- Crops the image
	- Displays the processed image in a window

	Parameters:
		path_to_image (str): Path to the image.
		threshold (int): Threshold value for binarization.
		crop_fraction (float): Fraction of the image dimensions to crop from each side.
	"""
	image = cv2.imread(path_to_image)
	if image is None:
		print(f"Warning: Unable to read {path_to_image}")
	else:
		gray_image = grayscale(image)
		binary_image = binarize_image(gray_image, threshold)
		cropped_image = crop_image(binary_image, crop_fraction)

		cv2.imshow("image", cropped_image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()


def process_directory(path_to_directory, threshold=160, crop_fraction=0):
	"""
	Processes every image in a specified directory:
	- Converts image to grayscale
	- Applies binary thresholding
	- Crops the image
	- Saves the processed images in an 'images_improved' subfolder

	Parameters:
		path_to_directory (str): Path to the directory.
		threshold (int): Threshold value for binarization.
        crop_fraction (float): Fraction of the image dimensions to crop from each side.
        
	Directory Structure:
		directory/
			├── images/
			│   └── image1.jpg
			├── images_improved/
			│   └── improved_image1.jpg
	"""
	path_to_images = os.path.join(path_to_directory, "images")
	output_directory = os.path.join(path_to_directory, 'images_improved')
	os.makedirs(output_directory, exist_ok=True)

	for image_name in tqdm(os.listdir(path_to_images), total=len(os.listdir(path_to_images)), unit="image", desc="Binarizing Images", ncols=100):
		path_to_image = os.path.join(path_to_images, image_name)
		image = cv2.imread(path_to_image)
		gray_image = grayscale(image)
		binary_image = binarize_image(gray_image, threshold)
		cropped_image = crop_image(binary_image, crop_fraction)
			
		output_file_path = os.path.join(output_directory, f"improved_{image_name}")
		cv2.imwrite(output_file_path, cropped_image)
		#print(f"Processed and saved: {output_file_path}")
       

threshold = 158
crop_fraction = 0.025

# Process one image
path_to_image = "data/1854/images/1854_page_0043.jpg"
#process_image(path_to_image, threshold, crop_fraction)

# Process images in one directory
path_to_directory = "data/1931"
process_directory(path_to_directory, threshold, crop_fraction)

# Process images in all directories
root_directory = "data"
#process_images_in_directory(root_directory, threshold, crop_fraction)