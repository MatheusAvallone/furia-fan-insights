# twitter_api.py

import requests
from typing import List

# Função para buscar tweets com base em uma palavra-chave
def buscar_tweets(sobre_o_que: str) -> List[str]:
    url = f"https://api.twitter.com/2/tweets/search/recent?query={sobre_o_que}"
    headers = {"Authorization": "Bearer SEU_TOKEN_DO_TWITTER"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        tweets = response.json()["data"]
        return [tweet["text"] for tweet in tweets]
    else:
        return []
