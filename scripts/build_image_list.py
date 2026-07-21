import pandas as pd

INPUT = "data/category_summary.csv"
OUTPUT = "data/image_download_list.csv"

df = pd.read_csv(INPUT)

# Clean text
for col in [
    "Manufacturer",
    "RepresentativeModel",
    "Generic Group",
    "Generic SubType"
]:
    df[col] = df[col].fillna("").astype(str).str.strip()

# Build search query
df["SearchQuery"] = (
    df["Manufacturer"] + " " + df["RepresentativeModel"]
).str.strip()

# Build image filename
df["ImageFile"] = (
    df["Generic Group"]
    .str.lower()
    .str.replace(" ", "_", regex=False)
    + "_"
    +
    df["Generic SubType"]
    .str.lower()
    .str.replace(" ", "_", regex=False)
)

df["ImageFile"] = (
    df["ImageFile"]
    .str.strip("_")
    + ".jpg"
)

# Remove duplicates
df = df.drop_duplicates(
    subset=["ImageFile"]
)

df.to_csv(
    OUTPUT,
    index=False
)

print(f"Images required: {len(df)}")
print(f"Output: {OUTPUT}")