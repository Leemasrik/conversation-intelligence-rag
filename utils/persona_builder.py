import json
import os
import re

from utils.parser import load_conversations, parse_conversation


def extract_persona(messages):

    user_messages = [
        m["text"]
        for m in messages
        if m["speaker"] == "User 1"
    ]

    text = " ".join(user_messages).lower()

    #################################################

    habits = []

    habit_words = [
        "always",
        "usually",
        "often",
        "every day",
        "daily",
        "love",
        "enjoy",
        "like"
    ]

    for sentence in user_messages:

        if any(word in sentence.lower() for word in habit_words):
            habits.append(sentence)

    #################################################

    personal_facts = []

    patterns = [

        r"i am ([^.!,]+)",

        r"i'm ([^.!,]+)",

        r"i work as ([^.!,]+)",

        r"my job is ([^.!,]+)",

        r"i live in ([^.!,]+)",

        r"i have ([^.!,]+)"

    ]

    for pattern in patterns:

        personal_facts.extend(
            re.findall(pattern, text)
        )

    #################################################

    avg_words = sum(
        len(x.split())
        for x in user_messages
    ) / max(len(user_messages),1)

    style = "Short"

    if avg_words > 12:
        style = "Medium"

    if avg_words > 25:
        style = "Long"

    #################################################

    personality=[]

    if len(habits)>3:
        personality.append("Expressive")

    if avg_words>15:
        personality.append("Detailed")

    #################################################

    return {

        "habits": habits[:10],

        "personal_facts": list(set(personal_facts))[:10],

        "personality_traits": personality,

        "communication_style":{

            "message_length":style,

            "tone":"Friendly"

        }

    }


def build_personas(csv_path):

    conversations=load_conversations(csv_path)

    personas=[]

    global_id=1

    for cid,conversation in enumerate(conversations):

        messages,global_id=parse_conversation(
            conversation,
            global_id
        )

        persona=extract_persona(messages)

        persona["conversation_id"]=cid+1

        personas.append(persona)

    os.makedirs("persona",exist_ok=True)

    with open(
        "persona/personas.json",
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            personas,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("Personas Created")