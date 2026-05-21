import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

KOBIS_OPEN_API_KEY = os.getenv("KOBIS_OPEN_API_KEY")
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_CSV = BASE_DIR / "movie_data.csv"


def fetch_daily_boxoffice(target_date: str, item_count: int) -> list[dict]:
    """KOBIS 일별 박스오피스 API에서 데이터를 가져옵니다."""
    if not KOBIS_OPEN_API_KEY:
        raise ValueError(".env 파일에 KOBIS_OPEN_API_KEY를 설정해주세요.")

    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
    params = {
        "key": KOBIS_OPEN_API_KEY,
        "targetDt": target_date,
        "itemPerPage": str(item_count),
    }

    response = requests.get(url=url, params=params, timeout=15)
    response.raise_for_status()

    payload = response.json()
    return payload.get("boxOfficeResult", {}).get("dailyBoxOfficeList", [])


def fetch_movie_info(movie_code: str) -> dict:
    """KOBIS 영화상세 API에서 감독/장르 정보를 가져옵니다."""
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"
    params = {
        "key": KOBIS_OPEN_API_KEY,
        "movieCd": movie_code,
    }

    response = requests.get(url=url, params=params, timeout=15)
    response.raise_for_status()

    payload = response.json()
    return payload.get("movieInfoResult", {}).get("movieInfo", {})


def convert_to_app_schema(boxoffice_rows: list[dict]) -> pd.DataFrame:
    """Streamlit 앱에서 바로 사용할 수 있는 컬럼 구조로 변환합니다."""
    rows = []

    for movie in boxoffice_rows:
        title = movie.get("movieNm", "제목 없음")
        movie_code = movie.get("movieCd", "")

        movie_info = fetch_movie_info(movie_code) if movie_code else {}

        directors = movie_info.get("directors", [])
        artist = ", ".join(
            director.get("peopleNm", "") for director in directors if director.get("peopleNm")
        )

        genres = movie_info.get("genres", [])
        genre = ", ".join(
            genre_item.get("genreNm", "") for genre_item in genres if genre_item.get("genreNm")
        )

        open_date = movie.get("openDt", "")
        year = int(open_date[:4]) if len(open_date) >= 4 and open_date[:4].isdigit() else 0

        rank_text = str(movie.get("rank", "0"))
        rank = int(rank_text) if rank_text.isdigit() else 0
        score = max(1, 11 - rank) if rank > 0 else 1

        audi_acc_text = str(movie.get("audiAcc", "0")).replace(",", "")
        sales_point = int(audi_acc_text) if audi_acc_text.isdigit() else 0

        rows.append(
            {
                "title": title,
                "artist": artist,
                "genre": genre,
                "year": year,
                "score": score,
                "salesPoint": sales_point,
            }
        )

    return pd.DataFrame(rows)


def save_movie_csv(target_date: str = "20260520", item_count: int = 10) -> Path:
    """지정 날짜/개수로 movie_data.csv를 생성합니다."""
    boxoffice_rows = fetch_daily_boxoffice(target_date=target_date, item_count=item_count)
    movie_df = convert_to_app_schema(boxoffice_rows)
    movie_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    return OUTPUT_CSV


if __name__ == "__main__":
    output_path = save_movie_csv(target_date="20260520", item_count=10)
    print(f"CSV 생성 완료: {output_path}")
