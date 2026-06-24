import json
import csv
import os

INPUT_FILE = "training/data_full.json"
OUTPUT_FILE = "training/intent_dataset.csv"


INTENT_MAP = {

    # ---------------- Reminder ----------------

    "timer": "reminder",
    "alarm": "reminder",
    "calendar": "reminder",
    "calendar_update": "reminder",
    "schedule_meeting": "reminder",
    "pto_request": "reminder",

    # ---------------- Action ----------------

    "translate": "action-item",
    "transfer": "action-item",
    "restaurant_reservation": "action-item",
    "shopping_list_update": "action-item",
    "change_language": "action-item",
    "find_phone": "action-item",
    "email": "action-item",
    "todo_list": "action-item",
    "book_flight": "action-item",
    "book_hotel": "action-item",

    # ---------------- Small Talk ----------------

    "greeting": "small-talk",
    "goodbye": "small-talk",
    "thank_you": "small-talk",
    "tell_joke": "small-talk",
    "who_are_you": "small-talk",
    "who_made_you": "small-talk",
    "what_can_i_ask_you": "small-talk",
    "change_user_name": "small-talk",
    "where_are_you_from": "small-talk",

    # ---------------- Emotional ----------------

    "meaning_of_life": "emotional-support",

}
def convert_split(split, writer):

    total = 0

    for text, intent in split:

        label = INTENT_MAP.get(intent)

        if label is None:

            label = "unknown"

        writer.writerow([text, label])

        total += 1

    return total


def main():

    with open(INPUT_FILE, encoding="utf8") as f:

        data = json.load(f)

    os.makedirs("training", exist_ok=True)

    total = 0

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf8"
    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(["text", "intent"])

        for split in data:

            total += convert_split(
                data[split],
                writer
            )

    print("Dataset Created")

    print("Samples :", total)


if __name__ == "__main__":

    main()