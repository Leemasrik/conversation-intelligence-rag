from utils.parser import load_conversations, parse_conversation
from utils.summarizer import summarize_topic

conversations = load_conversations("data/conversations.csv")

messages, _ = parse_conversation(conversations[0], 1)

result = summarize_topic(messages)

print(result)