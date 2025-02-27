import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_image(path):
    """Load an image from file and convert to grayscale."""
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Error: Unable to load image at {path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, gray

def compute_diff(old_gray, new_gray):
    """Compute pixel-level difference and threshold it."""
    diff = cv2.absdiff(old_gray, new_gray)
    _, diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    return diff

def highlight_differences(new_image, diff):
    """Draw bounding boxes around differences."""
    contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 1 and h > 3:  # Avoid noise
            cv2.rectangle(new_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return new_image

def display(image):
    """Display an image using Matplotlib."""
    plt.figure(figsize=(10, 5))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()

def process_images(old_path, new_path):
    """Main function to process and compare drawings."""
    old_image, old_gray = load_image(old_path)
    new_image, new_gray = load_image(new_path)

    diff = compute_diff(old_gray, new_gray)
    highlighted_image = highlight_differences(new_image.copy(), diff)

    return highlighted_image
