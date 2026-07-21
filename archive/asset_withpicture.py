import os

IMAGE_FOLDER = "images"

count = len([
    f for f in os.listdir(IMAGE_FOLDER)
    if f.lower().endswith((
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ))
])

print(f"Existing images: {count}")