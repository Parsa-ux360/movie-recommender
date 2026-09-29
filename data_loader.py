import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(BASE_DIR, "data", "movies.csv")


def load_movies(path=DEFAULT_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")

    if os.path.getsize(path) == 0:
        raise ValueError(f"Dataset is empty: {path}")

    df = pd.read_csv(path)

    required = ['id', 'title', 'year', 'genres', 'director',
                'cast', 'overview', 'rating']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df['genres'] = df['genres'].fillna('')
    df['director'] = df['director'].fillna('')
    df['cast'] = df['cast'].fillna('')
    df['overview'] = df['overview'].fillna('')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)
    df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)

    if 'poster' not in df.columns:
        df['poster'] = ''
    df['poster'] = df['poster'].fillna('')

    return df


def create_soup(df):
    df['soup'] = (
        df['genres'].str.replace(',', ' ', regex=False) * 3 + " " +
        df['director'].str.replace(',', ' ', regex=False) * 2 + " " +
        df['cast'].str.replace(',', ' ', regex=False) + " " +
        df['overview']
    )
    return df