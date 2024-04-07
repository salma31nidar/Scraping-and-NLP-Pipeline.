import nltk
import stanza
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['lab1']
lemmatized_tokens_without_stopwords_collection = db['lemmatized_tokens_without_stopwords']
pos_tags_stanza_collection = db['pos_tags_stanza']
pos_tags_nltk_collection = db['pos_tags_nltk']

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Initialize Stanza pipeline for POS tagging
stanza.download('ar')
nlp = stanza.Pipeline(lang='ar', processors='tokenize,pos')

# Retrieve documents from the collection
documents = lemmatized_tokens_without_stopwords_collection.find()

# Check if there are documents in the collection

for document in documents:
        # Get lemmatized tokens from the document
        lemmatized_tokens = document['tokens']

        # Join lemmatized tokens into a single string
        text = ' '.join(lemmatized_tokens)

        # Process the text with Stanza for POS tagging
        doc_stanza = nlp(text)

        # Extract POS tags using Stanza
        pos_tags_stanza = [(word.text, word.upos) for sentence in doc_stanza.sentences for word in sentence.words]

        # Apply POS tagging using NLTK
        tokens = nltk.word_tokenize(text)
        pos_tags_nltk = nltk.pos_tag(tokens, tagset='universal')

        # Insert POS tags obtained from Stanza into the collection
        pos_tags_stanza_collection.insert_one({'document_id': document['_id'], 'pos_tags': pos_tags_stanza})

        # Insert POS tags obtained from NLTK into the collection
        pos_tags_nltk_collection.insert_one({'document_id': document['_id'], 'pos_tags': pos_tags_nltk})

print("POS tags for documents saved successfully.")

