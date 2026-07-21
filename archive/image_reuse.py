import pandas as pd

df = pd.read_csv(
    "data/datos_enriched.csv",
    engine="python",
    usecols=[
        "Generic Group",
        "Generic SubType",
        "image_path"
    ]
)

df = df.dropna(subset=["image_path"])

df = df[
    df["image_path"]
    .astype(str)
    .str.strip()
    != ""
]

category_images = (
    df.groupby(
        ["Generic Group", "Generic SubType"]
    )["image_path"]
    .first()
    .reset_index()
)

category_images.to_csv(
    "data/existing_category_images.csv",
    index=False
)

print(
    f"Categories already covered: "
    f"{len(category_images)}"
)