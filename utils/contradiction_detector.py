NEGATIONS = [
    "not",
    "never",
    "no",
    "don't",
    "didn't",
    "isn't",
    "wasn't",
    "can't"
]


def detect_contradictions(chunks):

    contradictions = []

    for i in range(len(chunks)-1):

        first = str(chunks[i]).lower()
        second = str(chunks[i+1]).lower()

        first_negative = any(
            word in first
            for word in NEGATIONS
        )

        second_negative = any(
            word in second
            for word in NEGATIONS
        )

        if first_negative != second_negative:

            contradictions.append({

                "earlier": chunks[i],

                "later": chunks[i+1]

            })

    return contradictions