import pandas as pd

FILE = "data/datos_enriched.csv"

df = pd.read_csv(FILE, low_memory=False)

df.columns = df.columns.str.strip()

# MTW only
mtw = df[
    df["Client"] ==
    "Maidstone and Tunbridge Wells NHS Trust"
].copy()

# Remove Graveyard assets
mtw = mtw[
    mtw["Site"]
    .fillna("")
    .str.strip()
    .str.lower()
    != "graveyard"
]

# Optional: remove missing/scrapped departments
mtw = mtw[
    ~mtw["Department"]
    .fillna("")
    .str.strip()
    .str.lower()
    .isin([
        "missing",
        "scrapped"
    ])
]

# Remove empty categories
mtw = mtw.dropna(
    subset=["Generic Group", "Generic SubType"],
    how="all"
)

# Create key
mtw["CategoryKey"] = (
    mtw["Generic Group"]
    .fillna("")
    .str.strip()
    + "|"
    +
    mtw["Generic SubType"]
    .fillna("")
    .str.strip()
)

summary = (
    mtw.groupby(
        ["Generic Group", "Generic SubType"]
    )
    .agg(
        AssetCount=("Asset ID", "count"),
        Manufacturer=("Manufacturer", lambda x: x.mode().iloc[0] if not x.mode().empty else ""),
        RepresentativeModel=("Description", lambda x: x.mode().iloc[0] if not x.mode().empty else "")
    )
    .reset_index()
)

summary["ImageFilename"] = (
    summary["Generic Group"]
    .fillna("")
    .str.lower()
    .str.replace(" ", "_", regex=False)
    + "_"
    +
    summary["Generic SubType"]
    .fillna("")
    .str.lower()
    .str.replace(" ", "_", regex=False)
    + ".jpg"
)

summary["SearchQuery"] = (
    summary["Manufacturer"].fillna("")
    + " "
    + summary["RepresentativeModel"].fillna("")
)

summary = summary.sort_values(
    "AssetCount",
    ascending=False
)

summary.to_csv(
    "data/category_summary.csv",
    index=False
)

print()
print(f"Total categories: {len(summary)}")
print()
print(summary.head(20))
print()
print("Saved:")
print("data/category_summary.csv")