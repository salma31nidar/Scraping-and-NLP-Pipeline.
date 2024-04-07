# Scraping-and-NLP-Pipeline.
## 1- Scraping from server Arabic web sources :
To scrape articles I utilizes Scrapy, Selenium, and BeautifulSoup to scrape news articles from the Arabic news website Al Jazeera. It begins by initializing a Scrapy spider with the start URL set to the news section of Al Jazeera's website. The spider employs Selenium to simulate user interaction by scrolling down the page and clicking a "See More" button to dynamically load additional articles. After each click, it waits for the content to load before parsing the HTML using BeautifulSoup. It extracts the URLs of individual articles and sends requests to each URL to extract the article header and content. Finally, it stores the extracted data, including the article URL, header, and content, into a MongoDB database. Upon completion, the Selenium WebDriver is closed. This script provides an automated solution for scraping Arabic news articles from Al Jazeera, facilitating further analysis or processing of the gathered information.
## 2- Store the raw data on a NoSql database “MongoDB”:
The concept involves storing the raw data obtained from scraping Arabic news articles in a NoSQL database, specifically MongoDB. This approach allows for the preservation of the scraped data in its original form, including the article URLs, headers, and content. By utilizing MongoDB, a flexible document-oriented database, the script can efficiently store and manage unstructured data without the need for predefined schemas. This facilitates easy retrieval and analysis of the scraped information, enabling further processing or analysis downstream. Additionally, MongoDB's scalability and robustness make it suitable for handling large volumes of data, ensuring that the scraped data can be effectively managed and accessed as needed.
## 3- Establishment of NLP Pipeline (Text Cleaning, Tokenization, Stop words, Discretization,Normalization) :
### 3-1  Text Cleaning:
The pipeline begins with text cleaning operations to standardize the Arabic text. This includes normalizing Arabic characters, removing diacritics, and removing punctuations.
### 3-2 Tokenization:
The cleaned text is tokenized into individual words using NLTK's word_tokenize function.
### 3-3 Lemmatization:
The tokenized words undergo lemmatization using Stanza, which normalizes each word to its base form (lemma). This step accounts for variations in word forms and improves the consistency of analysis.
### 3-4 Stemming:
The remaining tokens undergo stemming using the ISRIStemmer, which reduces each word to its root or stem. Stemming helps to further normalize the text and reduce the dimensionality of the data.
### 3-5 Stopwords Removal:
A list of Arabic stopwords is loaded from a text file (list.txt). These stopwords, common words that do not carry significant meaning, are removed from the tokenized text.
### 3-6 Storing Results:
The processed tokens are stored in separate collections within the MongoDB database. One collection stores lemmatized tokens without stopwords (lemmatized_tokens_without_stopwords), while another stores stemmed tokens without stopwords (Stemmed_Tokens_without_stopwords).
## 4- Comparison between Stemming and Lemmatization :
Both stemming and lemmatization serve as valuable preprocessing techniques in NLP tasks, lemmatization is generally preferred when accuracy and linguistic precision are paramount. Its consideration of context and part of speech enables it to produce more linguistically accurate results, making it suitable for applications requiring nuanced language understanding and semantic analysis. However, in situations where computational efficiency is a primary concern and a less precise approximation of word roots is acceptable, stemming may offer a faster and simpler alternative.
## 5- Parts of Speech technics based on both Rule based and Machine learning approaches :
Stanza, a modern NLP library, is utilized to tokenize and tag the text, extracting POS tags for each word. Stanza's approach involves deep learning models trained specifically for Arabic, providing accurate and detailed POS tagging results.

On the other hand, NLTK, a traditional NLP library, offers its own POS tagging functionality. In the script, NLTK is used to tokenize the text and assign universal POS tags to each token. While NLTK may not be as advanced as Stanza, it remains a popular choice for POS tagging due to its simplicity and ease of use.

After extracting POS tags from both libraries, the script stores the results in a MongoDB database, allowing for easy access and further analysis of the POS-tagged data. This approach enables researchers and practitioners to compare the performance of different POS tagging methods and choose the most suitable one for their specific needs.

## 6- NER Methods :
NER is a subtask of information extraction that aims to identify and classify named entities within a text into predefined categories such as names of persons, organizations, locations, dates, etc. The concept of NER involves analyzing text to detect and classify these entities, providing valuable insights for various applications such as information retrieval, question answering, and sentiment analysis.

In the code, the Stanza library is utilized to process Arabic text and extract named entities along with their corresponding labels. The script iterates through documents retrieved from a MongoDB collection, tokenizes the text, and applies Stanza's NER pipeline to identify named entities. The identified entities and their labels are then printed for further analysis or processing.

Overall, the code demonstrates a practical implementation of NER, allowing for the automatic identification and extraction of named entities from Arabic text data, thereby facilitating various downstream NLP tasks and analyses.
