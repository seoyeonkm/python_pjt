from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import requests


BASE_DIR = Path(__file__).resolve().parent
ITUNES_SEARCH_URL = "https://itunes.apple.com/search"


def fetch_itunes_music(term: str, limit: int, country: str = "KR") -> List[Dict[str, str]]:
    """Fetch music track data from the iTunes Search API."""
    params = {
        "term": term,
        "media": "music",
        "entity": "song",
        "limit": max(1, min(limit, 200)),
        "country": country,
        "lang": "ko_kr",
    }
    response = requests.get(ITUNES_SEARCH_URL, params=params, timeout=20)
    response.raise_for_status()

    payload = response.json()
    return payload.get("results", [])


def build_rows(results: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Normalize API response into a CSV schema compatible with Streamlit table use."""
    rows: List[Dict[str, object]] = []
    for item in results:
        release_date = str(item.get("releaseDate", ""))
        year = None
        if release_date:
            try:
                year = datetime.fromisoformat(release_date.replace("Z", "+00:00")).year
            except ValueError:
                year = None

        rows.append(
            {
                "title": item.get("trackName") or "",
                "artist": item.get("artistName") or "",
                "genre": item.get("primaryGenreName") or "기타",
                "year": year,
                "salesPoint": item.get("trackPrice") or item.get("collectionPrice") or 0,
                "category": "music",
                "country": item.get("country") or "",
                "currency": item.get("currency") or "",
                "previewUrl": item.get("previewUrl") or "",
                "artworkUrl": item.get("artworkUrl100") or "",
                "trackViewUrl": item.get("trackViewUrl") or "",
            }
        )
    return rows


def save_csv(rows: List[Dict[str, object]], output_file: Path) -> None:
    """Save collected rows as UTF-8 CSV."""
    fieldnames = [
        "title",
        "artist",
        "genre",
        "year",
        "salesPoint",
        "category",
        "country",
        "currency",
        "previewUrl",
        "artworkUrl",
        "trackViewUrl",
    ]
    with output_file.open("w", newline="", encoding="utf-8-sig") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="iTunes API에서 음악 데이터를 받아 music_data.csv를 생성합니다."
    )
    parser.add_argument("--term", default="kpop", help="검색 키워드 (기본값: kpop)")
    parser.add_argument("--limit", type=int, default=100, help="저장할 데이터 수 (기본값: 100)")
    parser.add_argument(
        "--country",
        default="KR",
        help="국가 코드 (기본값: KR, 예: US, JP)",
    )
    parser.add_argument(
        "--output",
        default="music_data.csv",
        help="저장할 CSV 파일명 (기본값: music_data.csv)",
    )
    args = parser.parse_args()

    output_path = BASE_DIR / args.output

    try:
        results = fetch_itunes_music(term=args.term, limit=args.limit, country=args.country)
        rows = build_rows(results)
        save_csv(rows, output_path)
    except requests.RequestException as exc:
        print(f"[ERROR] iTunes API 요청 실패: {exc}")
        return

    print(f"[DONE] 저장 완료: {output_path}")
    print(f"[DONE] 저장 건수: {len(rows)}")


if __name__ == "__main__":
    main()
