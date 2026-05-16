import requests
import os
from dotenv import load_dotenv

load_dotenv()

ALADIN_OPEN_API_KEY = os.getenv("ALADIN_OPEN_API_KEY")
item_list_url = "https://www.aladin.co.kr/ttb/api/ItemList.aspx"

item_list_params = {
    "ttbkey": ALADIN_OPEN_API_KEY,
    "QueryType": "BestSeller",
    "SearchTarget": "Book",
    #"subSearchTarget":
    #"start":
    #"MaxReasults":
    #"Cover":
    #"CategoryId":
    "output": "js",
    #"Partner":
    #"includeKey":
    #"InputEncoding":
    "Version": "20131101",
    #"outofStockFilter":
    #"Year,Month,Week":
}

response = requests.get(url=item_list_url, params=item_list_params)
print(response.text)