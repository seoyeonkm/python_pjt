import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

import requests

url = "https://api.themoviedb.org/3/movie/popular"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZmVmYzNkZTk1OTEzOWQ4ZTdiYWIzMWQwMDc2MTA1YSIsIm5iZiI6MTc3ODkzMTI3My43MSwic3ViIjoiNmEwODU2NDllYTA2MWEwNzVmNjY0M2IzIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.g6yVrbVf5V9gjapMm_KJ3X2BOAnBvcHYWPhhm4X5R1c"
}

response = requests.get(url, headers=headers)

print(response.text)