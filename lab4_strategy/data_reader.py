import requests


class RevenueBudgetReader:
    def __init__(self, dataset_url):
        self.dataset_url = dataset_url

    def read_data(self):
        response = requests.get(self.dataset_url, timeout=20)
        response.raise_for_status()
        return response.json()
