import json
import os

from utils.parser import load_conversations, parse_conversation


def create_chunks(
    csv_path,
    chunk_size=20,
    output_file="summaries/chunks.json"
):

    conversations = load_conversations(csv_path)

    chunks = []

    global_message_id = 1

    chunk_id = 1

    for conversation in conversations:   # Remove [:20] later

        messages, global_message_id = parse_conversation(
            conversation,
            global_message_id
        )

        for i in range(0, len(messages), chunk_size):

            chunk = messages[i:i+chunk_size]

            if len(chunk) == 0:
                continue

            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "start_message": chunk[0]["message_id"],
                    "end_message": chunk[-1]["message_id"],
                    "text": " ".join(
                        [
                            m["text"]
                            for m in chunk
                        ]
                    )
                }
            )

            chunk_id += 1

    os.makedirs("summaries", exist_ok=True)

    with open(
        output_file,
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"Created {len(chunks)} chunks")