import pandas as pd
import os
import re

DATA_PATH = "data/datos.csv"
IMAGE_FOLDER = "images"


def clean_filename(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_') + ".jpg"


def update_csv():
    df = pd.read_csv(DATA_PATH)

    # ✅ Normalize column names
    df.columns = df.columns.str.strip()

    # ✅ Add column if it doesn't exist
    if "image_path" not in df.columns:
        df["image_path"] = ""

    for i, row in df.iterrows():
        description = row["Description"]

        # Skip invalid descriptions
        if pd.isna(description) or str(description).strip() == "":
            continue

        description = str(description).strip()

        filename = clean_filename(description)
        filepath = os.path.join(IMAGE_FOLDER, filename)

        if os.path.exists(filepath):
            df.at[i, "image_path"] = f"images/{filename}"
        else:
            # Optional: set default image
            # df.at[i, "image_path"] = "images/no_image.jpg"
            pass

    # ✅ Save updated CSV
    df.to_csv(DATA_PATH, index=False)

    print("✅ CSV updated with image paths!")


if __name__ == "__main__":
    update_csv()