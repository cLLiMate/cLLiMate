import functools

import gensim.downloader
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer


def init_nltk():
    nltk.download("stopwords")
    nltk.download("wordnet")
    nltk.download("omw-1.4")


def process_sentence(sentences):
    """Generator to process multiple sentences into tokens."""
    stop_words = set(stopwords.words("english"))
    tokenizer = RegexpTokenizer(r"\w+")
    lemmatizer = WordNetLemmatizer()

    for sentence in sentences:
        tokens = tokenizer.tokenize(sentence)
        tokens = [token.lower() for token in tokens if token not in stop_words]
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        yield tokens


@functools.cache
def get_glove_vector(model_name="glove-wiki-gigaword-50"):
    init_nltk()
    return gensim.downloader.load(model_name)


def embed_sentence(glove_vector, sentence):
    """Embed a sentence into a vector space by averaging them."""
    tokens = next(process_sentence([sentence]))
    return glove_vector[[t for t in tokens if t in glove_vector]].mean(axis=0)
