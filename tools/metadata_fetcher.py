import requests

def fetch_metadata(title: str) -> dict:
    try:
        url = "https://api.crossref.org/works"
        params = {"query.title": title, "rows": 1}
        r = requests.get(url, params=params, timeout=5)
        if r.status_code == 200:
            item = r.json()['message']['items'][0]
            return {
                "title": item.get('title', [''])[0],
                "year": item.get('created', {}).get('date-parts', [[None]])[0][0],
                "doi": item.get('DOI')
            }
    except:
        return None
    return None
