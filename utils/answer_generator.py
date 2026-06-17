import re


def get_best_sentence(text, patterns):

    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Ignore greetings and short sentences
    ignore = [
        "hi",
        "hello",
        "thanks",
        "thank you",
        "good",
        "great",
        "nice",
        "cool",
        "awesome",
        "okay",
        "ok"
    ]

    best = None

    for sentence in sentences:

        s = sentence.strip()

        if len(s) < 25:
            continue

        if any(s.lower().startswith(word) for word in ignore):
            continue

        for pattern in patterns:

            if re.search(pattern, s, re.IGNORECASE):

                return s

        if best is None:
            best = s

    return best


def generate_answer(query, results, persona=None):

    query = query.lower()

    if not results["topics"]:
        return "No relevant information was found."

    topic = results["topics"][0]

    summary = topic["summary"]

    text = " ".join(topic.get("messages", []))

    # ------------------------------------
    # Moving / Location
    # ------------------------------------

    if any(x in query for x in [
        "where",
        "moving",
        "relocate",
        "city",
        "country"
    ]):
        
        patterns = [
            r"moving to\s+([A-Za-z\s,]+?)(?:\.|!|\?|$)",
            r"relocating to\s+([A-Za-z\s,]+?)(?:\.|!|\?|$)",
            r"live in\s+([A-Za-z\s,]+?)(?:\.|!|\?|$)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                place = match.group(1).strip()
                return f"The user is moving to {place}."

        sentence = get_best_sentence(
            text,
            [
                r"moving to",
                r"relocat",
                r"live in",
                r"from"
            ]
        )

        return sentence or summary

    # ------------------------------------
    # Job
    # ------------------------------------

    elif any(x in query for x in [
        "job",
        "work",
        "profession",
        "career"
    ]):

        sentence = get_best_sentence(
            text,
            [
                r"i am a",
                r"i'm a",
                r"i work",
                r"working as",
                r"firefighter",
                r"teacher",
                r"engineer",
                r"doctor",
                r"nurse",
                r"librarian",
                r"barista",
                r"tutor",
                r"artist"
            ]
        )

        return sentence or summary

    # ------------------------------------
    # Pets
    # ------------------------------------

    elif any(x in query for x in [
        "dog",
        "cat",
        "pet",
        "animal"
    ]):

        sentence = get_best_sentence(
            text,
            [
                r"dog",
                r"cat",
                r"pet",
                r"puppy"
            ]
        )

        return sentence or summary

    # ------------------------------------
    # Hobbies
    # ------------------------------------

    elif any(x in query for x in [
        "hobby",
        "hobbies",
        "enjoy",
        "love",
        "like"
    ]):

        sentence = get_best_sentence(
            text,
            [
                r"i love",
                r"i enjoy",
                r"i like",
                r"my hobby"
            ]
        )

        return sentence or summary

    # ------------------------------------
    # Habits
    # ------------------------------------

    elif "habit" in query:

        if persona and persona["habits"]:

            return "\n".join(
                f"• {h}"
                for h in persona["habits"][:5]
            )

        return "No habits were identified."

    # ------------------------------------
    # Personality
    # ------------------------------------

    elif "personality" in query or "person" in query:

        if persona and persona["personality_traits"]:

            return "The user appears to be " + ", ".join(
                persona["personality_traits"]
            )

        return "Personality could not be determined."

    # ------------------------------------
    # Communication
    # ------------------------------------

    elif "communicat" in query or "talk" in query:

        if persona:

            style = persona["communication_style"]

            return (
                f"Message Length: {style['message_length']}\n"
                f"Tone: {style['tone']}"
            )

        return "Communication style unavailable."

    # ------------------------------------
    # Personal facts
    # ------------------------------------

    elif "fact" in query:

        if persona and persona["personal_facts"]:

            return "\n".join(
                f"• {f}"
                for f in persona["personal_facts"][:5]
            )

        return "No personal facts found."

    # ------------------------------------
    # Default
    # ------------------------------------

    return summary