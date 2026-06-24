import pandas as pd

df = pd.read_csv("training/intent_dataset.csv")

print(df["intent"].value_counts())