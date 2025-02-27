import os
from services.image_processing import process_images, display

# Sample images (update paths as needed)
old_image_path = "data/old_drawing.jpg"
new_image_path = "data/new_drawing.jpg"

if not os.path.exists(old_image_path) or not os.path.exists(new_image_path):
    print("Error: Image files not found in the 'data/' folder.")
else:
    print("Processing images...")
    result = process_images(old_image_path, new_image_path)
    display(result)
    print("Processing complete.")
