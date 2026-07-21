import pandas as pd
from rapidfuzz import process, fuzz

missing = pd.read_csv(
    "data/top_missing_descriptions.csv"
)

models = pd.read_csv(
    "data/model_list.csv",
    usecols=[
        "Description",
        "Generic Group",
        "Generic SubType"
    ],
    low_memory=False
)

model_descriptions = (
    models["Description"]
    .fillna("")
    .astype(str)
    .tolist()
)

results = []

for desc in missing["Description"].dropna():

    match = process.extractOne(
        str(desc),
        model_descriptions,
        scorer=fuzz.token_sort_ratio
    )

    if match:

        model_row = models[
            models["Description"] == match[0]
        ].iloc[0]

        results.append({
            "Missing Description": desc,
            "Matched Model": match[0],
            "Score": match[1],
            "Generic Group": model_row["Generic Group"],
            "Generic SubType": model_row["Generic SubType"]
        })

result_df = pd.DataFrame(results)

result_df.to_csv(
    "data/fuzzy_matches.csv",
    index=False
)

print(result_df.head(20))
print()
print(f"Matches found: {len(result_df)}")