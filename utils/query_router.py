from utils.answer_generator import (
    generate_answer,
    generate_conflict_answer
)

from utils.conflict_resolver import resolve

from utils.intent_classifier import predict_intent


CONFLICT_WORDS = [

    "mention",

    "mentioned",

    "remember",

    "talk about",

    "did i",

    "anything about"

]


def is_conflict_query(query):

    query = query.lower()

    return any(
        word in query
        for word in CONFLICT_WORDS
    )


def route_query(
    query,
    results,
    persona
):

    intent = predict_intent(query)

    if is_conflict_query(query):

        conflict = resolve(query)

        return generate_conflict_answer(
            conflict
        )

    return generate_answer(
        query,
        results,
        persona
    )