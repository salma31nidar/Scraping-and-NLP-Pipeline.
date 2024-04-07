import stanza
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['lab1']
lemmatized_tokens_without_stopwords_collection = db['lemmatized_tokens_without_stopwords']

# Download the Arabic model for Stanza
stanza.download('ar')

# Initialize Stanza for Arabic
nlp = stanza.Pipeline(lang='ar', processors='tokenize,ner')

# Retrieve documents from the collection
documents = lemmatized_tokens_without_stopwords_collection.find()

    # Iterate over each document
for document in documents:
        # Get the tokens from the document
        tokens = document['tokens']

        # Join the tokens into a single string
        text = ' '.join(tokens)

        # Process the text with Stanza
        doc = nlp(text)

        # Extract named entities and their labels
        named_entities = []
        for sentence in doc.sentences:
            for entity in sentence.ents:
                named_entities.append((entity.text, entity.type))

        # Print named entities and their labels
        for entity in named_entities:
            print(entity)
