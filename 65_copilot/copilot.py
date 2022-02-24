import os
import sys
import time
import json
import requests
import urllib.request
import urllib.parse
import urllib.error

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

def download_json(url):
    """Download a JSON file from a URL and return the data."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']

