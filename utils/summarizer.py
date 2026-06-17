from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from rake_nltk import Rake


def summarize_topic(messages):

    text = " ".join(m["text"] for m in messages)

    parser = PlaintextParser.from_string(
        text,
        Tokenizer("english")
    )

    summarizer = TextRankSummarizer()

    summary = " ".join(
        str(sentence)
        for sentence in summarizer(parser.document, 3)
    )

    rake = Rake()

    rake.extract_keywords_from_text(text)

    keywords = rake.get_ranked_phrases()[:8]

    return {
        "summary": summary,
        "keywords": keywords
    }