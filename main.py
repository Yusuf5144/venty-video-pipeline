# main.py
from sheet_client import get_next_draft, update_row
from render import build_video

def run_pipeline():
    # 1) Nächste Zeile mit Status "draft" finden
    row, script = get_next_draft()
    if not row:
        print("Keine Drafts gefunden.")
        return

    print(f"Verarbeite Zeile {row}: {script[:30]}…")

    # 2) Video bauen
    video_file = f"video_{row}.mp4"
    build_video(script, video_file)

    # 3) (Simulation) Video-URL erzeugen
    video_url = f"https://cdn.example.com/videos/{video_file}"

    # 4) Sheet updaten
    update_row(row, "video_url", video_url)
    update_row(row, "status", "ready")

    print(f"Zeile {row} fertig – status=ready, video_url gesetzt")

if __name__ == "__main__":
    run_pipeline()
