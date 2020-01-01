# docsearcx | A minimal document search engine.
docsearcx is a simple search engine that retrives information from ***pdfs*** based on term frequency-inverse Document frequency and cosine similarity to retrive relevant documents.


## Limitation
For the sake of POC this application relies on in memory storage.

---

## Setup
### Installing Pipenv
If pipenv is already installed skip this step.

```pip install pipenv```

### Installing Dependencies

```pipenv install```

& Activate the virtual environment shell by

```pipenv shell```

### Running the Flask app

```python app.py```

### Term Frequency-inverse Document Frequency
TF-IDF is a numerical statistics which reflects how important a word is to a document. The tf-idf value increases proportionally to the number of times a word appears in the document, but is offset by the frequency of the word in the corpus, which helps to control for the fact that some words are generally more common than others.