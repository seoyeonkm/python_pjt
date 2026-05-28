import os

import pandas as pd
import requests


TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TARGET_COUNT = 100

TMDB_DISCOVER_URL = "https://api.themoviedb.org/3/discover/movie"
TMDB_GENRE_URL = "https://api.themoviedb.org/3/genre/movie/list"


def get_genre_map(language="ko-KR"):
    params = {
        "api_key": TMDB_API_KEY,
        "language": language,
    }
    response = requests.get(TMDB_GENRE_URL, params=params, timeout=20)
    response.raise_for_status()

    genre_map = {}
    for genre in response.json().get("genres", []):
        genre_id = genre.get("id")
        if genre_id is not None:
            genre_map[genre_id] = genre.get("name", "기타")
    return genre_map


def get_tmdb_movies(target_count=TARGET_COUNT, language="ko-KR"):
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY 환경변수를 설정해주세요.")

    genre_map = get_genre_map(language=language)
    all_movies = []
    seen_ids = set()
    page = 1

    while len(all_movies) < target_count and page <= 500:
        params = {
            "api_key": TMDB_API_KEY,
            "language": language,
            "sort_by": "popularity.desc",
            "include_adult": "false",
            "include_video": "false",
            "page": page,
        }

        response = requests.get(TMDB_DISCOVER_URL, params=params, timeout=20)
        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            break

        for item in results:
            movie_id = item.get("id")
            if movie_id in seen_ids:
                continue

            seen_ids.add(movie_id)

            release_date = str(item.get("release_date") or "")
            year = int(release_date[:4]) if len(release_date) >= 4 and release_date[:4].isdigit() else 0

            genre_names = [genre_map.get(genre_id, "기타") for genre_id in item.get("genre_ids", [])]
            genre = ", ".join(genre_names) if genre_names else "기타"

            vote_average = float(item.get("vote_average") or 0)
            popularity = float(item.get("popularity") or 0)

            all_movies.append(
                {
                    "title": item.get("title") or "제목 없음",
                    "genre": genre,
                    "year": year,
                    "score": round(vote_average, 1),
                    "salesPoint": int(popularity * 1000),
                }
            )
        
        page += 1

    return pd.DataFrame(all_movies)


df = get_tmdb_movies()
df.to_csv("movie_data.csv", index=False, encoding="utf-8-sig")
print("--- TMDB 영화 데이터 수집 완료 ---")
