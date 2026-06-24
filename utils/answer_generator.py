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



    elif "habit" in query:

        if persona and persona["habits"]:

            return "\n".join(
                f"• {h}"
                for h in persona["habits"][:5]
            )

        return "No habits were identified."



    elif "personality" in query or "person" in query:

        if persona and persona["personality_traits"]:
            return "The user appears to be " + ", ".join(persona["personality_traits"])

        return (
            "The user appears to communicate in a "
            f"{persona['communication_style']['tone']} tone "
            f"with {persona['communication_style']['message_length'].lower()} messages."
        )

 

    elif any(word in query for word in [
            "communicate",
            "communication",
            "communicat",
            "talk",
            "speaks",
            "speaking",
            "conversation"
        ]):


        if persona:

            style = persona["communication_style"]

            return (
                f"Message Length: {style['message_length']}\n"
                f"Tone: {style['tone']}"
            )

        return "Communication style unavailable."

 

    elif "fact" in query:

        if persona and persona["personal_facts"]:

            return "\n".join(
                f"• {f}"
                for f in persona["personal_facts"][:5]
            )

        return "No personal facts found."

  
    return summary

def generate_conflict_answer(conflict_result):

    if conflict_result is None:
        return "No relevant information found."

    output = []

    output.append(f"🔍 Query Entity : {conflict_result['entity']}\n")

    output.append("=" * 60)

    # Current Understanding
    output.append("\n🧠 Current Understanding\n")

    timeline = conflict_result["timeline"]
    latest = timeline[-1]["summary"]

    output.append(
        f"The user mentioned **{conflict_result['entity']}** across multiple conversations. "
        "The retrieved memories have been ordered chronologically and analyzed for consistency.\n"
    )

    output.append(f"Latest Memory:\n{latest}")

    output.append("\n" + "=" * 60)

    # Timeline
    output.append("\n📅 Timeline\n")

    for topic in timeline:

        output.append(
            f"\nConversation {topic['conversation_id']}"
        )

        output.append(
            f"Messages : {topic['start_message']} - {topic['end_message']}"
        )

        output.append(
            f"Summary : {topic['summary']}"
        )

    output.append("\n" + "=" * 60)

    # Evidence
    output.append("\n📌 Supporting Evidence\n")

    for chunk in conflict_result["evidence"]:

        output.append(f"• {chunk['text']}")

    output.append("\n" + "=" * 60)

    # Contradictions
    output.append("\n⚠ Conflict Analysis\n")

    if conflict_result["conflicts"]:

        output.append(
            "Some retrieved conversations contain inconsistent information."
        )

        output.append(
            "This is expected because the dataset consists of independent conversations collected across different days."
        )

        output.append(
            "The system therefore presents the latest and most relevant information while flagging possible inconsistencies."
        )

    else:

        output.append(
            "No significant contradictions were detected across the retrieved conversations."
        )

    output.append("\n" + "=" * 60)

    # Final Conclusion
    output.append("\n✅ Final Conclusion\n")

    output.append(
        "The response was generated by combining:\n"
        "• Topic Checkpoints\n"
        "• Retrieved Message Chunks\n"
        "• Chronological Ordering\n"
        "• Emotion-Based Ranking\n"
        "• Conflict Detection\n"
    )

    return "\n".join(output)