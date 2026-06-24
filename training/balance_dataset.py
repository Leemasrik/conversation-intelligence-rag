import pandas as pd

# Load dataset
df = pd.read_csv("training/intent_dataset.csv")

# Separate classes
unknown = df[df["intent"] == "unknown"]
action = df[df["intent"] == "action-item"]
small = df[df["intent"] == "small-talk"]
reminder = df[df["intent"] == "reminder"]
emotion = df[df["intent"] == "emotional-support"]

# Reduce unknown class
unknown = unknown.sample(
    n=2500,
    random_state=42
)

# Combine
balanced = pd.concat([
    unknown,
    action,
    small,
    reminder,
    emotion
])

# Shuffle
balanced = balanced.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# Save
balanced.to_csv(
    "training/intent_dataset_balanced.csv",
    index=False
)

print(balanced["intent"].value_counts())
print("\nTotal Samples:", len(balanced))