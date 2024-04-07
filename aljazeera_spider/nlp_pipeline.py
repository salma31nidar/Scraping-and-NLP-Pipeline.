from pymongo import MongoClient
import re
import string
from nltk.tokenize import word_tokenize
import stanza
from nltk.stem import ISRIStemmer

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['lab1']
collection = db['eljazzira']
Stemmed_Tokens_without_stopwords = db['Stemmed_Tokens_without_stopwords']
lemmatized_tokens_without_stopwords = db['lemmatized_tokens_without_stopwords']

# Read the stop words file
with open('list.txt', 'r', encoding='utf-8') as file:
    stop_words = set(file.read().splitlines())

# Initialize Stanza pipeline for lemmatization
stanza.download('ar')
nlp = stanza.Pipeline(lang='ar', processors='tokenize,mwt,pos,lemma')

# Initialize ISRIStemmer for stemming
stemmer = ISRIStemmer()

# Retrieve the first document from the collection
document = collection.find()


def normalize_arabic(text):
        text = re.sub("[إأآا]", "ا", text)
        text = re.sub("ى", "ي", text)
        text = re.sub("ؤ", "ء", text)
        text = re.sub("ئ", "ء", text)
        text = re.sub("ة", "ه", text)
        text = re.sub("گ", "ك", text)
        return text


def remove_diacritics(text):
        arabic_diacritics = re.compile("""
                                         ّ    | # Tashdid
                                         َ    | # Fatha
                                         ً    | # Tanwin Fath
                                         ُ    | # Damma
                                         ٌ    | # Tanwin Damm
                                         ِ    | # Kasra
                                         ٍ    | # Tanwin Kasr
                                         ْ    | # Sukun
                                         ـ     # Tatwil/Kashid
                                     """, re.VERBOSE)
        return re.sub(arabic_diacritics, '', text)


def remove_punctuations(text):
        arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
        english_punctuations = string.punctuation
        punctuations_list = arabic_punctuations + english_punctuations
        translator = str.maketrans('', '', punctuations_list)
        return text.translate(translator)


def remove_repeating_char(text):
        return re.sub(r'(.)\1+', r'\1', text)


def tokenize_text(text):
        return word_tokenize(text)

documents = collection.find()
for document in documents:
    # Apply text processing functions
    cleaned_text = document['content']
    cleaned_text = normalize_arabic(cleaned_text)
    cleaned_text = remove_punctuations(cleaned_text)
    cleaned_text = remove_repeating_char(cleaned_text)

    # Tokenization
    tokens = tokenize_text(cleaned_text)

    # Lemmatization
    doc = nlp(cleaned_text)
    lemmatized_tokens = [word.lemma for sentence in doc.sentences for word in sentence.words]

    # Remove diacritics from lemmatized tokens
    lemmatized_tokens_without_diacritics = [remove_diacritics(token) for token in lemmatized_tokens]

    # Stemming
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    # Remove stop words
    tokens_without_stopwords = [word for word in tokens if word not in stop_words]
    lemmatized_tokens_without_stopwords = [word for word in lemmatized_tokens_without_diacritics if
                                           word not in stop_words]
    stemmed_tokens_without_stopwords = [word for word in stemmed_tokens if word not in stop_words]

    # Store lemmatized tokens without stopwords in a new collection
    db['lemmatized_tokens_without_stopwords'].insert_one({'tokens': lemmatized_tokens_without_stopwords})

    # Store stemmed tokens without stopwords in another collection
    db['Stemmed_Tokens_without_stopwords'].insert_one({'tokens': stemmed_tokens_without_stopwords})

# Close the client connection
client.close()