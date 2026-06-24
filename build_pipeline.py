import json
import os

from utils.parser import load_conversations, parse_conversation
from utils.topic_detector import detect_topics
from utils.summarizer import summarize_topic

os.makedirs("summaries", exist_ok=True)

conversations = load_conversations("data/conversations.csv")

topic_summaries = []
checkpoints = []

global_message_id = 1
checkpoint_buffer = []

# IMPORTANT:
# During testing process only first 20 conversations
# Later remove [:20]

for conversation_id, conversation in enumerate(conversations):

    print(f"Processing Conversation {conversation_id+1}")

    messages, global_message_id = parse_conversation(
        conversation,
        global_message_id
    )

  

    topic_ranges = detect_topics(messages)

    for topic in topic_ranges:

        topic_messages = messages[
            topic["start"]:topic["end"]+1
        ]

        result = summarize_topic(topic_messages)

        topic_summaries.append(
            {
                "conversation_id": conversation_id+1,
                "topic_id": len(topic_summaries)+1,
                "start_message": topic_messages[0]["message_id"],
                "end_message": topic_messages[-1]["message_id"],
                "summary": result["summary"],
                "keywords": result["keywords"],
                "messages": [
                    m["text"] for m in topic_messages
                ]
            }
        )

 
    for message in messages:

        checkpoint_buffer.append(message)

        if len(checkpoint_buffer) == 100:

            result = summarize_topic(checkpoint_buffer)

            checkpoints.append(
                {
                    "checkpoint_id": len(checkpoints)+1,
                    "start_message": checkpoint_buffer[0]["message_id"],
                    "end_message": checkpoint_buffer[-1]["message_id"],
                    "summary": result["summary"],
                    "keywords": result["keywords"]
                }
            )

            checkpoint_buffer = []



with open(
    "summaries/topic_summaries.json",
    "w",
    encoding="utf8"
) as f:

    json.dump(
        topic_summaries,
        f,
        indent=4,
        ensure_ascii=False
    )

with open(
    "summaries/checkpoints.json",
    "w",
    encoding="utf8"
) as f:

    json.dump(
        checkpoints,
        f,
        indent=4,
        ensure_ascii=False
    )

print("Finished")