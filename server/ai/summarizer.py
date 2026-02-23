import nltk
import heapq
import re

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


def summarize_text(text: str, max_sentences: int = 3) -> str:
    if not text or len(text.split()) < 30:
        return text

    # Clean text
    text = re.sub(r'\s+', ' ', text)

    # Sentence tokenize
    sentences = sent_tokenize(text)

    # Word tokenize
    words = word_tokenize(text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    word_frequencies = {}

    for word in words:
        if word.isalnum() and word not in stop_words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

    if not word_frequencies:
        return " ".join(sentences[:max_sentences])

    # Normalize frequencies
    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    # Score sentences
    sentence_scores = {}

    for sent in sentences:
        sent_words = word_tokenize(sent.lower())
        for word in sent_words:
            if word in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

    # Pick top sentences
    summary_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)

    # Preserve original order
    summary = " ".join([s for s in sentences if s in summary_sentences])

    return summary