def build_timeline(chunks):
    """
    Sort retrieved chunks chronologically.
    """

    timeline = sorted(
        chunks,
        key=lambda x: x.get("conversation_id", 0)
    )

    return timeline