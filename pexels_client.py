# pexels_client.py
from dotenv import load_dotenv
import os, requests

load_dotenv()

PEXELS_KEY = os.getenv("PEXELS_API_KEY")
if not PEXELS_KEY:
    raise RuntimeError("PEXELS_API_KEY fehlt in der .env!")

HEADERS = {
    "Authorization": PEXELS_KEY
}

def fetch_clips(query: str, per_page: int = 3) -> list[str]:
    """
    Ruft über die Pexels Video Search API bis zu `per_page` Clips zum `query` ab
    und gibt eine Liste von MP4-Download-Links zurück.
    """
    url = "https://api.pexels.com/videos/search"
    params = {
        "query": query,
        "per_page": per_page
    }
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    urls = []
    for vid in data.get("videos", []):
        # nimm die erste verfügbare Qualität
        files = vid.get("video_files", [])
        if files:
            urls.append(files[0]["link"])
    return urls
