import pandas as pd

df = pd.read_csv("data/model_list.csv")

groups = sorted(df["Generic Group"].dropna().unique())

print(f"Total Generic Groups: {len(groups)}")

for group in groups:
    print(group)