import sys
import re
import math
import collections
from nltk import PorterStemmer
from pdf_reader import readAllPdf

class Engine:

    def __init__(self):
        self.ps = PorterStemmer() #* Initiate porterstemmer from nltk
        self.alphanum = re.compile('[^a-zA-Z0-9]') #* For the text pre-processing
        self.titles = [] #* For storing filenames -> abspaths
        self.docs = [] #* For storing the content for ranking and searching
        self.vocab = [] #* For storing the extracted vocab from the pdfs

    def get_uniq_words(self):
        """
        * @desc: Get all the uinque words from the documents
        * @return: List on unique words
        """
        uniq = set()
        for doc in self.docs:
            for word in doc:
                uniq.add(word)
        return uniq

    def read_raw_data(self):
        """
        * @desc: Reads and process the raw data aka without stemming and get the data ready for processing
        * @return: List of (filename, content) after stemming and preprocessing it
        """
        docs = []
        title = []
        for filename, content in readAllPdf():
            current_filename = filename
            content = content.lower() #* Making sure everything is lower
            content = [line.strip() for line in content.split()] #* Splitting on whitespaces
            content = [self.alphanum.sub('', word) for word in content] #* Removing non alphanumeric characters
            content = [word for word in content if word != ''] #* Remove any words that are now empty due to splitting them and and getting them through re
            content = [self.ps.stem(word) for word in content] #* Stem words
            docs.append(content)
            title.append(filename)

        return title, docs

    def read_data(self):
        """
        * @desc: Reads in the documents to be indexed.
        * @return: None
        """
        titles, docs = self.read_raw_data()
        #* Sort document alphabetically by title to ensure we have the proper
        #* document indices when referring to them.
        ordering = [idx for idx, title in sorted(enumerate(titles), key = lambda xx : xx[1])]

        self.titles = []
        self.docs = []
        numdocs = len(docs)
        for d in range(numdocs):
            self.titles.append(titles[ordering[d]])
            self.docs.append(docs[ordering[d]])

        #* Get the vocabulary.
        self.vocab = [word for word in self.get_uniq_words()]

    def compute_tfidf(self):
        """
        * @desc: Compute and store TF-IDF values for words and documents.
        """
        self.tfidf = {}
        idf = {}
        doc_cont = {}

        for i, doc in enumerate(self.docs):
            doc_cont[i] = collections.Counter(doc)
        for word in self.vocab:
            word_set = 0.0 + len(Engine.get_posting(self, word))
            idf[word] = math.log10(len(self.docs) / word_set)
            if word not in self.tfidf:
                self.tfidf[word] = {}
            for d in range(len(self.docs)):
                tf = doc_cont[d][word]
                if tf == 0.0:
                    self.tfidf[word][d] = 0.0
                else:
                    self.tfidf[word][d] = (1.0 + math.log10(tf)) * idf[word]

    def get_tfidf(self, word, document):
        """
        * @desc: Return the tf-idf weigthing for the given word (string) and document index.
        """
        tfidf = self.tfidf[word][document]
        return tfidf

    def get_tfidf_unstemmed(self, word, document):
        """
        * @desc: This function gets the TF-IDF of an *unstemmed* word in a document.
        *        Stems the word and then calls get_tfidf.
        """
        word = self.p.stem(word)
        return self.get_tfidf(word, document)

    def index(self):
        """
        *@desc: Build an index of the documents.
        """
        print("Indexing...")

        inv_index = {}

        #* Create a list for each word
        for word in self.vocab:
                inv_index[word] = []

        #* Copy the index of document where the word is
        for i, doc in enumerate(self.docs):
            for word in set(doc):
                    inv_index[word].append(i)

        self.inv_index = inv_index
        print("Indexing...Completed!")

    def get_posting(self, word):
        """
        * @desc: Given a word, this returns the list of document indices (sorted) in
        *        which the word occurs.
        """
        posting = []

        #* Return the list of the given word
        posting = self.inv_index[word]
        set(posting)
        sorted(posting)

        return posting

    def get_posting_unstemmed(self, word):
        """
        * @desc: Given a word, this *stems* the word and then calls get_posting on the
        *        stemmed word to get its postings list.
        """
        word = self.p.stem(word)
        return self.get_posting(word)

    def boolean_retrieve(self, query):
        """
        * @desc: Given a query in the form of a list of *stemmed* words, this returns
        *        the list of documents in which *all* of those words occur (ie an AND query).
        * @return: an empty list if the query does not return any documents.
        """

        docs = []
        words_list = []

        #* Store in words_list the inv_index of each word of the query
        for word in query:
            words_list.append(set(self.inv_index[word]))

        #* Intersect the words_list in a list with the common documents
        docs = reduce(lambda x,y: x & y, words_list)

        return sorted(docs)

    def rank_retrieve(self, query):
        """
        * @desc: Given a query (a list of words), return a rank-ordered list of documents (by ID) and score for the query.
        * @return: List of rank ordered list
        *@ ref: https://stackoverflow.com/questions/22724164/cosine-similarity-python
        """
        scores = [0.0 for xx in range(len(self.docs))]

        q_count = {}

        #* Calculate a counter of term-frecuency in query
        q_count = collections.Counter(query)


        numerator = 0.0
        denominator = 0.0
        for d, doc in enumerate(self.docs):
            intersec = set(query).intersection(set(doc))
            for word in intersec:
                qt = (1.0 + math.log10(q_count[word]))
                dt = self.get_tfidf(word, d)
                numerator = numerator + qt*dt

            for word in set(doc):
                dd = self.get_tfidf(word, d)
                denominator = denominator + dd*dd

            scores[d] = numerator/math.sqrt(denominator)

        ranking = [idx for idx, sim in sorted(enumerate(scores), key = lambda xx : xx[1], reverse = True)]
        results = []
        for i in range(20):
            results.append((ranking[i], scores[ranking[i]]))
        return results

    def process_query(self, query_str):
        """
        * @desc: Given a query string, process it and return the list of lowercase, alphanumeric, stemmed words in the string.
        """
        query = query_str.lower() #* make sure everything is lower case
        query = query.split() #* split on whitespace
        query = [self.alphanum.sub('', xx) for xx in query] #* remove non alphanumeric characters
        query = [self.ps.stem(xx) for xx in query] #* stem words
        return query


    def query_retrieve(self, query_str):
        """
        * @desc: Given a string, process and then return the list of matching documents found by boolean_retrieve().
        """
        query = self.process_query(query_str)
        return self.boolean_retrieve(query)


    def query_rank(self, query_str):
        """
        * @desc: Given a string, process and then return the list of the top matching documents, rank-ordered.
        """
        query = self.process_query(query_str)
        return self.rank_retrieve(query)


""" Only for testing """
def main(args):
    engine = Engine()
    engine.read_data()
    engine.index()
    engine.compute_tfidf()
    query = " ".join(args)
    print("Best matching documents to '%s':" % query)
    results = engine.query_rank(query)
    for docId, score in results:
        print("%s: %e" % (engine.titles[docId], score))

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
