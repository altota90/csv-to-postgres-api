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

df = df.dropna(
    subset=[
        "Generic Group",
        "Generic SubType",
        "image_path"
    ]
)

df = df[
    df["image_path"]
    .astype(str)
    .str.strip()
    != ""
]

categories = (
    df[
        ["Generic Group", "Generic SubType"]
    ]
    .drop_duplicates()
)

print(
    f"Categories with existing images: "
    f"{len(categories)}"
)