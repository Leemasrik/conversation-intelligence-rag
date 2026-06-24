import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import csv

from utils.parser import load_conversations, parse_conversation


def detect_intent(text):

    text = text.lower()

    reminder_words = [
        "remind",
        "remember",
        "tomorrow",
        "later",
        "next week",
        "next month",
        "don't forget",
        "schedule"
    ]

    emotional_words = [
        "sad",
        "upset",
        "depressed",
        "angry",
        "lonely",
        "anxious",
        "stress",
        "cry",
        "worried",
        "help me"
    ]

    action_words = [
        "book",
        "buy",
        "call",
        "send",
        "email",
        "order",
        "find",
        "search",
        "create",
        "make",
        "build",
        "write",
        "generate"
    ]

    smalltalk_words = [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good evening",
        "how are you",
        "thanks",
        "thank you",
        "bye",
        "good night"
    ]

    if any(word in text for word in reminder_words):
        return "reminder"

    if any(word in text for word in emotional_words):
        return "emotional-support"

    if any(word in text for word in action_words):
        return "action-item"

    if any(word in text for word in smalltalk_words):
        return "small-talk"

    return "unknown"


def build_dataset():

    conversations = load_conversations("data/conversations.csv")

    global_id = 1

    rows = []

    for conversation in conversations:

        messages, global_id = parse_conversation(
            conversation,
            global_id
        )

        for message in messages:

            if message["speaker"] != "User 1":
                continue

            intent = detect_intent(message["text"])

            rows.append([
                message["text"],
                intent
            ])

    os.makedirs("training", exist_ok=True)

    with open(
        "training/intent_dataset.csv",
        "w",
        newline="",
        encoding="utf8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "text",
            "intent"
        ])

        writer.writerows(rows)

    print(f"Dataset Created : {len(rows)} samples")


if __name__ == "__main__":

    build_dataset()