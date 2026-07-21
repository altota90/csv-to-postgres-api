import pandas as pd

ASSET_FILE = "data/datos.csv"
MODEL_FILE = "data/model_list.csv"
OUTPUT_FILE = "data/datos_enriched.csv"


def build_lookup(models_df):
    lookup = {}

    for _, row in models_df.iterrows():
        description = str(row["Description"]).strip()

        lookup[description] = {
            "group": row.get("Generic Group", ""),
            "subtype": row.get("Generic SubType", "")
        }

    return lookup


def enrich_assets():
    assets = pd.read_csv(
    ASSET_FILE,
    engine="python"
)
    models = pd.read_csv(MODEL_FILE)

    # Remove accidental spaces in headers
    assets.columns = assets.columns.str.strip()
    models.columns = models.columns.str.strip()

    lookup = build_lookup(models)

    assets["Generic Group"] = ""
    assets["Generic SubType"] = ""

    matches = 0

    print("Loading assets...")

    for i, row in assets.iterrows():

        description = str(row["Description"]).strip()

        if description in lookup:

            assets.at[i, "Generic Group"] = lookup[description]["group"]
            assets.at[i, "Generic SubType"] = lookup[description]["subtype"]

            matches += 1

    assets.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✅ Matching complete")
    print(f"✅ Matches found: {matches}")
    print(f"✅ Output saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    enrich_assets()