# test_pexels.py
from pexels_client import fetch_clips

if __name__ == "__main__":
    clips = fetch_clips("hibiscus tea", per_page=3)
    print("Gefundene Clips:", clips)
