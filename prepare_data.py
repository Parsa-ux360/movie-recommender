import pandas as pd
import json
import ast
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

MOVIES_CSV = os.path.join(DATA_DIR, "tmdb_5000_movies.csv")
CREDITS_CSV = os.path.join(DATA_DIR, "tmdb_5000_credits.csv")
OUTPUT_CSV = os.path.join(DATA_DIR, "movies.csv")


def safe_parse(value):
    if pd.isna(value):
        return []
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return []


def extract_names(value, limit=None):
    items = safe_parse(value)
    names = [item.get('name', '') for item in items if isinstance(item, dict)]
    names = [n for n in names if n]
    if limit:
        names = names[:limit]
    return ", ".join(names)


def extract_director(value):
    items = safe_parse(value)
    for item in items:
        if isinstance(item, dict) and item.get('job') == 'Director':
            return item.get('name', '')
    return ""


def build_dataset():
    if not os.path.exists(MOVIES_CSV):
        raise FileNotFoundError(f"Not found: {MOVIES_CSV}")
    if not os.path.exists(CREDITS_CSV):
        raise FileNotFoundError(f"Not found: {CREDITS_CSV}")

    print("Loading CSV files...")
    movies = pd.read_csv(MOVIES_CSV)
    credits = pd.read_csv(CREDITS_CSV)

    credits = credits.rename(columns={'movie_id': 'id'})
    credits = credits.drop(columns=['title'])
    df = movies.merge(credits, on='id')

    print("Extracting genres, cast, director...")
    df['genres'] = df['genres'].apply(extract_names)
    df['cast'] = df['cast'].apply(lambda x: extract_names(x, limit=5))
    df['director'] = df['crew'].apply(extract_director)

    df['year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
    df['year'] = df['year'].fillna(0).astype(int)

    df = df[df['overview'].notna()]
    df = df[df['overview'].str.strip() != '']

    final = pd.DataFrame({
        'id': df['id'],
        'title': df['title'],
        'year': df['year'],
        'genres': df['genres'],
        'director': df['director'],
        'cast': df['cast'],
        'overview': df['overview'],
        'rating': df['vote_average'],
    })

    final = final.drop_duplicates(subset='title').reset_index(drop=True)
    final = final[final['rating'] > 0]

    final.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(final)} movies to {OUTPUT_CSV}")


if __name__ == "__main__":
    build_dataset()