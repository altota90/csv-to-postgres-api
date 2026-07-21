import pandas as pd

df = pd.read_csv(
    "data/datos_enriched.csv",
    engine="python",
    usecols=[
        "Client",
        "Description",
        "Manufacturer",
        "Generic Group",
        "Generic SubType"
    ]
)

mtw = df[
    df["Client"] ==
    "Maidstone and Tunbridge Wells NHS Trust"
]

missing = mtw[
    mtw["Generic Group"]
    .fillna("")
    .str.strip()
    == ""
]

print(f"Missing records: {len(missing)}")

missing["Description"]\
    .value_counts()\
    .head(100)\
    .to_csv(
        "data/top_missing_descriptions.csv"
    )