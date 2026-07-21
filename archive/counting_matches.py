import pandas as pd

df = pd.read_csv(
    "data/datos_enriched.csv",
    engine="python",
)

mtw = df[
    df["Client"] ==
    "Maidstone and Tunbridge Wells NHS Trust"
]

total = len(mtw)

grouped = mtw[
    mtw["Generic Group"]
    .notna()
]

grouped = grouped[
    grouped["Generic Group"]
    .astype(str)
    .str.strip()
    != ""
]

print(f"Total MTW Assets: {total}")
print(f"Categorised Assets: {len(grouped)}")
print(
    f"Missing Categories: "
    f"{total - len(grouped)}"
)