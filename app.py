from flask import Flask, jsonify, request
from flask_cors import CORS
from engine import Engine
from storage import numberOfFiles

app = Flask(__name__)
CORS(app)

#* Initilize the query engine
engine = Engine()
engine.read_data()
engine.index()
engine.compute_tfidf()

@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({
        "number_of_files": numberOfFiles()
    })

@app.route('/api/search', methods=['GET'])
def search():
    search_term = request.args.get('q') #* get the search term requested
    query = " ".join(search_term)
    results = engine.rank_retrieve(query)
    result_buffer = []
    for docId, score in results:
        result_buffer.append([engine.titles[docId], score])
    return jsonify(result_buffer)

if __name__ == "__main__":
    app.run(debug=True)