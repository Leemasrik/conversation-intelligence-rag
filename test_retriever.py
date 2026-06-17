from utils.retriever import retrieve

results = retrieve(
    "Where is the user moving?"
)

print("\nTOPICS\n")

for t in results["topics"]:

    print("="*60)

    print(t["summary"])

print("\nCHUNKS\n")

for c in results["chunks"]:

    print("="*60)

    print(c["text"][:250])