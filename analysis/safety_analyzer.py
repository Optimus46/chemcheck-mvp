from ml.toxicity_model import predict_toxicity
def analyze_safety(ingredients):
    results = []

    for ing in ingredients:
        score = predict_toxicity(ing)
        results.append({
            "ingredient": ing,
            "toxicity_score": score,
            "risk": "High" if score > 0.6 else "Low"
        })

    return results
