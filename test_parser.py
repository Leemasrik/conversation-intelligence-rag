from utils.parser import load_conversations
from utils.parser import parse_conversation

conversations = load_conversations("data/conversations.csv")

print("Total Conversations:", len(conversations))

messages, next_id = parse_conversation(
    conversations[0],
    1
)

print(messages[:5])

print("Next ID:", next_id)