def evaluate(prompt, response):
    p = set(prompt.lower().split())
    r = set(response.lower().split())

    relevance = min(len(p & r) * 10, 100)
    clarity = 85 if len(response.split()) > 12 else 50
    accuracy = 80
    consistency = 75

    overall = (relevance + clarity + accuracy + consistency) / 4

    return {
        "relevance": relevance,
        "clarity": clarity,
        "accuracy": accuracy,
        "consistency": consistency,
        "overall": round(overall,2)
    }