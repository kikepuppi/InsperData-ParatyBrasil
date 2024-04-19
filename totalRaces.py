import requests
import numpy as np
from tqdm import tqdm
import json


url = f'https://api.utmb.world/search/races-qualifiers?lang=en&dateMin=1999-12-31&dateMax=2025-12-30&limit=43400'
page = requests.get(url)
races_dict = page.json()['races']

print(len(races_dict))

with open('corridas_total.json', 'w') as f:
    json.dump(races_dict, f)