import re
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
        * @return: 
        """
        docs = []
        for filename, content in readAllPdf():
            current_filename = filename
            lines = []
            content = content.lower() #* Making sure everything is lower
            content = [line.strip() for line in content.split()] #* Splitting on whitespaces
            content = [self.alphanum.sub('', word) for word in content] #* Removing non alphanumeric characters
            content = [word for word in content if word != ''] #* Remove any words that are now empty due to splitting them and and getting them through re
            content = [self.ps.stem(word) for word in content] #* Stem words
            if current_filename == filename:
                lines.extend(content)
            if current_filename != filename:
                docs.append((current_filename, lines))
                current_filename = filename
                continue
        print(docs)

if __name__ == "__main__":
    Engine().read_raw_data()

