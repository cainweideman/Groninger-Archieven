import os
import cv2
import argparse
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


def process_image(img_path, output_dir, threshold=160, crop=0):
    image = cv2.imread(img_path)
    img_name = os.path.splitext(os.path.basename(img_path))[0]
    gray_image = grayscale(image)
    binary_image = binarize_image(gray_image, threshold)
    cropped_image = crop_image(binary_image, crop)
        
    output_file_path = os.path.join(output_dir, f"binarized_{img_name}.jpg")
    cv2.imwrite(output_file_path, cropped_image)


def process_directory(input_path, output_dir, threshold=160, crop=0):
    image_files = []
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith(".jpg"):
                image_files.append(os.path.join(root, file))

    for img_path in tqdm(image_files, desc="Processing images"):
        process_image(img_path, output_dir, threshold, crop)


def main():
    parser = argparse.ArgumentParser(description="Binarize and crop a single image, directory, or nested directories.")
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to a single image, a directory of imagess, or a directory containing nested directories with images.")
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory. Default: 'binarized_images' in the current working directory.", default="./binarized_images")
    parser.add_argument("-t", "--threshold", type=int, help="Threshold value for binarization.", default=160)
    parser.add_argument("-c", "--crop", type=float, help="Fraction of the image dimensions to crop from each side.", default=0.0)

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
        process_image(input_path, output_dir, args.threshold, args.crop)
    elif os.path.isdir(input_path):
        # Directory or nested directories of PDFs
        print(f"Processing directory: {input_path}")
        process_directory(input_path, output_dir, args.threshold, args.crop)
    else:
        print(f"Error: The input path {input_path} does not exist or is not valid.")
        exit(1)

if __name__ == "__main__":
    main()