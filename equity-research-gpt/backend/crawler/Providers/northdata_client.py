import os, requests

BASE = os.getenv("NORTHDATA_BASE", "https://www.northdata.de/_api")
KEY = os.getenv("NORTHDATA_API_KEY")

class NorthDataClient:
    def __init__(self):
        if not KEY:
            raise RuntimeError("NORTHDATA_API_KEY not set")
    def _get(self, path, params):
        url = f"{BASE}{path}"
        # North Data akzeptiert api_key als Query-Parameter
        p = {"api_key": KEY}
        p.update({k:v for k,v in (params or {}).items() if v is not None})
        r = requests.get(url, params=p, timeout=30)
        r.raise_for_status()
        return r.json()
    def publications(self, source="bundesanzeiger", limit=10, pos=None,
                     minPublicationDate=None, maxPublicationDate=None,
                     countries=None, legalForm=None, eventType=None):
        return self._get("/pub/v1/publications", {
            "source": source,
            "limit": limit,
            "pos": pos,
            "minPublicationDate": minPublicationDate,
            "maxPublicationDate": maxPublicationDate,
            "countries": countries,
            "legalForm": legalForm,
            "eventType": eventType,
        })
