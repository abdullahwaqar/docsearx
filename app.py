from flask import Flask, jsonify, request
from engine import Engine

app = Flask(__name__)

#* Initilize the query engine
engine = Engine()
engine.read_data()
engine.index()
engine.compute_tfidf()

@app.route('/api/search', methods=['GET'])
def search():
    search_term = request.args.get('q')
    return search_term

if __name__ == "__main__":
    app.run(debug=True)