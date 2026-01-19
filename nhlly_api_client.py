import requests

def get_data(endpoint) -> dict:
    """
    Basic data fetching command
    Used in conjunction with endpoint to fetch data from Official NHL API
    """
    url = "https://api-web.nhle.com/v1/"
    r = requests.get(f"{url}{endpoint}")
    if r.status_code == 200:
        return r.json()
    else:
        return {"error": "Could not retrieve data"}