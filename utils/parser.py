import pandas as pd
import re

MESSAGE_PATTERN = r"(User\s+\d+):\s*(.*?)(?=(?:User\s+\d+:)|$)"


def load_conversations(csv_path):
    """
    Load CSV where each row contains one conversation.
    """
    df = pd.read_csv(csv_path, header=None)
    return df[0].dropna().tolist()


def parse_conversation(conversation, start_message_id=1):
    """
    Parse a single conversation into ordered messages.

    Returns:
        messages
        next_message_id
    """

    matches = re.findall(
        MESSAGE_PATTERN,
        conversation,
        flags=re.DOTALL,
    )

    messages = []

    current_id = start_message_id

    for speaker, text in matches:

        messages.append(
            {
                "message_id": current_id,
                "speaker": speaker.strip(),
                "text": text.strip(),
            }
        )

        current_id += 1

    return messages, current_id