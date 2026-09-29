from flask import Flask, render_template, request, jsonify
from recommender import MovieRecommender

app = Flask(__name__)
recommender = MovieRecommender()


@app.route('/')
def index():
    movies = recommender.get_all_titles()
    return render_template('index.html', movies=movies)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'results': []})

    results = recommender.search(query, limit=20)
    return jsonify({'results': results})

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    title = data.get('title', '')

    if not title:
        return jsonify({'error':'please choose a movie'}),404

    results = recommender.recommend(title, top_n=6)
    if not results:
        return jsonify({'error':'no movie was found'}),404


    return jsonify({'recommendations': results})

if __name__ == '__main__':
    app.run(debug=True)