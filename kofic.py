import os
import requests
from dotenv import load_dotenv

load_dotenv()

KOBIS_OPEN_API_KEY = os.getenv("KOBIS_OPEN_API_KEY")

movie_list_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
movie_item_list_params = {
    "key": KOBIS_OPEN_API_KEY, 
    "targetDt": "20260515",    
    "itemPerPage": "10",       
    "multiMovieYn": "",        
    "repNationCd": "",        
    "wideAreaCd": ""          
}

response = requests.get(url = movie_list_url, params = movie_item_list_params)
print(response.text)
