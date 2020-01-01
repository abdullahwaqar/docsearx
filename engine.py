import re
import collections
from nltk import PorterStemmer
from pdf_reader import readAllPdf

class Engine:

    def __init__(self):
        self.ps = PorterStemmer() #* Initiate porterstemmer from nltk
        self.alphanum = re.compile('[^a-zA-Z0-9]') #* For the text pre-processing
        self.filenames = [] #* For storing filenames -> abspaths
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
        ordering = [idx for idx, title in sorted(enumerate(titles),
        key = lambda xx : xx[1])]

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
        *
        """
        self.tfidf = {}
        idf = {}
        doc_cont = {}

        for i, doc in enumerate(self.docs):
            doc_cont[i] = collections.Counter(doc)
        for word in self.vocab:
            word_set = 0.0 + len(IRSystem.get_posting(self, word))
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


if __name__ == "__main__":
    Engine().read_data()

