import requests
from typing import List

def buscar_tweets(sobre_o_que: str, max_results: int = 10) -> List[str]:
    url = f"https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": "Bearer SEU_TOKEN_DO_TWITTER"}
    params = {
        "query": sobre_o_que,
        "max_results": max_results  # Defina quantos tweets retornar
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        tweets = response.json().get("data", [])
        return [tweet["text"] for tweet in tweets]
    else:
        # Logando erro
        print(f"Erro ao buscar tweets: {response.status_code} - {response.text}")
        return []

# Exemplo de uso
tweets = buscar_tweets("FURIA eSports")
print(tweets)
