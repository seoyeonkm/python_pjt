import os
import requests
from dotenv import load_dotenv

# .env 파일 로드 및 API 키 가져오기
load_dotenv()
KOBIS_OPEN_API_KEY = os.getenv("KOBIS_OPEN_API_KEY")

# 1. 기본 요청 URL (JSON 형식 지정)
movie_list_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"

# 2. 요청 파라미터 설정 (명세서 3번 항목 참조)
movie_item_list_params = {
    "key": KOBIS_OPEN_API_KEY,      # 필수: 발급받은 키
    "targetDt": "20260515",    # 필수: 조회하고자 하는 날짜 (YYYYMMDD)
    "itemPerPage": "10",       # 선택: 결과 개수 (최대 10)
    "multiMovieYn": "",        # 선택: "Y"(다양성), "N"(상업) (빈값은 전체)
    "repNationCd": "",         # 선택: "K"(한국), "F"(외국) (빈값은 전체)
    "wideAreaCd": ""           # 선택: 상영지역코드 (빈값은 전체)
}
response = requests.get(url = movie_list_url, params = movie_item_list_params)
print(response.text)
