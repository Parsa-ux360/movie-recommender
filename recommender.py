from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_loader import load_movies, create_soup


class MovieRecommender:
    def __init__(self):
        self.df = load_movies()
        self.df = create_soup(self.df)
        self._build_model()

    def _build_model(self):
        tfidf = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )

        tfidf_matrix = tfidf.fit_transform(self.df['soup'])
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def get_all_titles(self):
        data = self.df[['id', 'title', 'year', 'rating', 'genres', 'poster']].copy()
        data = data.sort_values('rating', ascending=False)
        return data.to_dict('records')

    def recommend(self, title, top_n=6):
        matches = self.df[self.df['title'].str.lower() == title.lower()]
        if matches.empty:
            return []

        idx = matches.index[0]
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n * 3 + 1]

        if not sim_scores:
            return []

        max_score = sim_scores[0][1]

        movie_indices = [i[0] for i in sim_scores]
        results = self.df.iloc[movie_indices][
            ['id', 'title', 'year', 'genres', 'rating', 'overview', 'poster']
        ].copy()

        results['similarity'] = [
            round((score / max_score) * 95, 1) if max_score > 0 else 0
            for _, score in sim_scores
        ]

        results = results[results['rating'] >= 6.0]
        results = results.head(top_n)

        return results.to_dict('records')

    def search(self, query, limit=20):
        if not query:
            return []
        mask = self.df['title'].str.contains(query, case=False, na=False)
        results = self.df[mask].head(limit)
        return results[['id', 'title', 'year', 'rating', 'genres', 'poster']].to_dict('records')
    
