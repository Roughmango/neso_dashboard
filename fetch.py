import requests


class Fetch:
    def fetch(self, url):
        response = requests.get(url)
        return response.json()["data"], response.status_code
