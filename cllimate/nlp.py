import nltk
from gensim.corpora import Dictionary
from gensim.models import LdaModel
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
