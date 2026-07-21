import pandas as pd

df = pd.read_csv("data/model_list.csv", low_memory=False)

print(
    df[["Generic Group", "Generic SubType"]]
    .drop_duplicates()
    .shape[0]
)