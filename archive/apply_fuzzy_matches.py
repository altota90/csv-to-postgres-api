import pandas as pd

ENRICHED_FILE = "data/datos_enriched.csv"
FUZZY_FILE = "data/fuzzy_matches.csv"
OUTPUT_FILE = "data/datos_enriched_v2.csv"

# Load files
assets = pd.read_csv(
    ENRICHED_FILE,
    engine="python"
)

matches = pd.read_csv(
    FUZZY_FILE
)

assets.columns = assets.columns.str.strip()
matches.columns = matches.columns.str.strip()

# Only keep high-confidence matches
matches = matches[
    matches["Score"] >= 85
]

# Build lookup
lookup = {}

for _, row in matches.iterrows():

    desc = str(
        row["Missing Description"]
    ).strip()

    lookup[desc] = {
        "group": row["Generic Group"],
        "subtype": row["Generic SubType"]
    }

updated = 0

for idx, row in assets.iterrows():

    group = str(
        row.get("Generic Group", "")
    ).strip()

    # Already categorised
    if group:
        continue

    description = str(
        row.get("Description", "")
    ).strip()

    if description not in lookup:
        continue

    assets.at[
        idx,
        "Generic Group"
    ] = lookup[description]["group"]

    assets.at[
        idx,
        "Generic SubType"
    ] = lookup[description]["subtype"]

    updated += 1

assets.to_csv(
    OUTPUT_FILE,
    index=False
)

print()
print(f"Assets updated : {updated}")
print(f"Saved file     : {OUTPUT_FILE}")
print()