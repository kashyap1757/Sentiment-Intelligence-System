import requests
import json

base_url = "http://127.0.0.1:8000/predict"

positive_review = {
    "review": "This movie was absolutely fantastic! The acting was superb and the plot was very engaging."
}

negative_review = {
    "review": "This was a terrible movie. The plot was boring and the acting was very poor."
}

pos_res = requests.post(base_url, json=positive_review)
neg_res = requests.post(base_url, json=negative_review)

results = {
    "positive_test": pos_res.json(),
    "negative_test": neg_res.json()
}

with open("api_results.json", "w") as f:
    json.dump(results, f, indent=4)

print("Results saved to api_results.json")
