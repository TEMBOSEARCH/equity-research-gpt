from providers import northdata

if __name__ == "__main__":
    # Einfacher Einmal-Lauf. Auf Render als Cron-Job mit:
    # python backend/crawler/main.py
    northdata.run_delta(limit=20)
    print("Crawler durchgelaufen.")
