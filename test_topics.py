from utils.parser import load_conversations, parse_conversation
from utils.topic_detector import detect_topics

conversations = load_conversations("data/conversations.csv")

messages, _ = parse_conversation(conversations[0], 1)

topics = detect_topics(messages)

print(topics)