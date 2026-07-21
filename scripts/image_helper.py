import pandas as pd
import webbrowser
import os
import time

DATA_PATH = "data/image_download_list.csv"
IMAGE_FOLDER = "images/category"


def open_image_search():

    df = pd.read_csv(DATA_PATH)

    df.columns = df.columns.str.strip()

    os.makedirs(IMAGE_FOLDER, exist_ok=True)

    total = len(df)

    for idx, row in df.iterrows():

        query = str(row["SearchQuery"]).strip()
        filename = str(row["ImageFile"]).strip()

        if not query:
            continue

        if not filename:
            continue

        filepath = os.path.join(
            IMAGE_FOLDER,
            filename
        )

        # Skip already downloaded images
        if os.path.exists(filepath):
            print(
                f"[{idx + 1}/{total}] "
                f"Skipping existing: {filename}"
            )
            continue

        # Bing Images search
        url = (
            "https://www.bing.com/images/search?q="
            + query.replace(" ", "+")
        )

        print("\n" + "=" * 50)
        print(f"[{idx + 1}/{total}]")
        print(f"Search Query : {query}")
        print(f"Save As      : {filename}")
        print(f"Location     : {filepath}")
        print("=" * 50 + "\n")

        webbrowser.open(url)

        input(
            "👉 Download the best image into the "
            "'images' folder using the filename above.\n"
            "Press ENTER when finished..."
        )

        time.sleep(1)


if __name__ == "__main__":
    open_image_search()