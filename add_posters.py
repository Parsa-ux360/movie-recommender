import pandas as pd
import requests
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MOVIES_CSV = os.path.join(DATA_DIR, "movies.csv")

TMDB_API_KEY = "dd99ee51fb66280eb0d7a0468bd6069d"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


def fetch_poster(movie_id):
    try:
        url = f"{BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"{IMAGE_BASE}{poster_path}"
        return ""
    except Exception as e:
        print(f"  Error for ID {movie_id}: {e}")
        return ""


def main():
    if TMDB_API_KEY == "YOUR_API_KEY_HERE":
        print("❌ Please set your TMDB_API_KEY first!")
        return

    print("Loading movies.csv...")
    df = pd.read_csv(MOVIES_CSV)

    if 'poster' not in df.columns:
        df['poster'] = ""

    total = len(df)
    print(f"Fetching posters for {total} movies...")
    print("This will take about 10-15 minutes. Please be patient.\n")

    for i, idx in enumerate(df.index):
        if df.at[idx, 'poster']:
            continue  

        poster_url = fetch_poster(df.at[idx, 'id'])
        df.at[idx, 'poster'] = poster_url

        if (i + 1) % 50 == 0:
            print(f"  Progress: {i + 1}/{total}")
            df.to_csv(MOVIES_CSV, index=False)  
            time.sleep(1)  

        time.sleep(0.1)  

    df.to_csv(MOVIES_CSV, index=False)
    print(f"\n✅ Done! Posters added to {MOVIES_CSV}")


if __name__ == "__main__":
    main()