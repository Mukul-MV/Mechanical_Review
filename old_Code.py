import cv2
import numpy as np
import pytesseract
from skimage.metrics import structural_similarity as ssim
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import os
from pdf2image import convert_from_path
!apt-get update
!apt-get install -y poppler-utils


def load_image(path):
    """Load an image from file and convert to grayscale."""
    print(f"Loading image: {path}")
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, gray

def convert_pdf_to_images(pdf_path):
    """Convert a PDF file to a list of image file paths."""
    print(f"Converting PDF to images: {pdf_path}")
    
    # Extract filename without extension
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # Convert PDF pages to images
    images = convert_from_path(pdf_path)
    
    output_paths = []
    for i, img in enumerate(images):
        output_path = f"/kaggle/working/{base_name}{i}.jpg"
        img.save(output_path, "JPEG")
        output_paths.append(output_path)
    
    return output_paths

def compute_diff(old_gray, new_gray):
    """Compute the pixel-level difference between two images."""
    print("Computing pixel-level difference...")
    diff = cv2.absdiff(old_gray, new_gray)
    _, diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)  # Threshold the diff to emphasize differences
    return diff


def highlight_differences(old_image, new_image, diff):
    """Highlight differences in the new image using red bounding boxes."""
    print("Highlighting differences in the new image...")
    # Find contours in the diff image
    contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 1 and h > 3:  # Lowered threshold to capture smaller changes
            cv2.rectangle(new_image, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Draw bounding box in red
    return new_image

def display(image):
    # Display Result
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 1, 1)
    plt.title("Differences Highlighted")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()
    
def get_file_extension(file_path: str) -> str:
    _, extension = os.path.splitext(file_path)
    return extension

def main(old_path, new_path):
    """Main function to process and compare drawings."""
    print("Starting drawing comparison...")
    is_pdf = get_file_extension(old_path) == ".pdf"
    if is_pdf:
        old_images = convert_pdf_to_images(old_path)
        new_images = convert_pdf_to_images(new_path)
        print("after pdf to image conversion imagesssss")
        display(old_images[0])
        display(new_images[0])
        old_image, old_gray = old_images[0], cv2.cvtColor(old_images[0], cv2.COLOR_BGR2GRAY)
        new_image, new_gray = new_images[0], cv2.cvtColor(new_images[0], cv2.COLOR_BGR2GRAY)
    else:
        old_image, old_gray = load_image(old_path)
        new_image, new_gray = load_image(new_path)
        print("after pdf to image conversion imagesssss")
        display(old_image)
        display(new_image)

    # Image Comparison
    diff = compute_diff(old_gray, new_gray)
    highlighted_image = highlight_differences(old_image.copy(), new_image.copy(), diff)
    
    # Display Result
    display(highlighted_image)
    
    print("Processing complete.")
    return 0

old_jpg = "/kaggle/input/adaptor/Adapte_old.jpg"
new_jpg = "/kaggle/input/adaptor/Adapte_copy.jpg"

main(old_jpg,new_jpg)