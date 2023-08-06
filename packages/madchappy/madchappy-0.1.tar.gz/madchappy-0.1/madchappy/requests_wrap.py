import requests

def get_data(url):
    return requests.get(url=url).json()

def post_data(url):
    return requests.post(url=url).json()
