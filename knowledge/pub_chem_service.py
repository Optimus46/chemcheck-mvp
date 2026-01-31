import requests

def fetch_chemical_data(ingredient):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{ingredient}/JSON"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None
