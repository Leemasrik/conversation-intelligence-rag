import pandas as pd

df = pd.read_csv("training/intent_dataset_balanced.csv")

emotion = df[df["intent"] == "emotional-support"].copy()

extra = []

prefixes = [
    "I feel ",
    "Honestly, ",
    "Today ",
    "Recently ",
    "Sometimes "
]

for _, row in emotion.iterrows():
    text = row["text"]

    for prefix in prefixes:
        extra.append({
            "text": prefix + text,
            "intent": "emotional-support"
        })

extra_df = pd.DataFrame(extra)

balanced = pd.concat([df, extra_df]).sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

balanced.to_csv(
    "training/intent_dataset_final.csv",
    index=False
)

print(balanced["intent"].value_counts())