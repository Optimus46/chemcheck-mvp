def predict_toxicity(ingredient):
    # 1. Normalize the text to lowercase so case doesn't matter
    ingredient = ingredient.lower().strip()
    
    # 2. Expand your list of harmful keywords
    harmful_keywords = [
        "paraben", 
        "formaldehyde", 
        "phthalate", 
        "sodium benzoate", 
        "sulfate", 
        "triclosan", 
        "benzene", 
        "oxybenzone", 
        "coal tar"
    ]

    # 3. Check if any harmful keyword appears INSIDE the ingredient name
    # (e.g., "methylparaben" will now be caught because it contains "paraben")
    for keyword in harmful_keywords:
        if keyword in ingredient:
            return 0.8  # High risk
            
    return 0.2  # Low risk