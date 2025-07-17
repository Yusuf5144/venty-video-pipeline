# test_import.py
try:
    import moviepy.editor
    print("moviepy.editor importiert ✅")
except Exception as e:
    print("Fehler beim Import von moviepy.editor:", e)
