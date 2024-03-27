import requests
import pandas as pd

def extract(extract_type, call, save_path):
    """
    Extracts data from a URL or an API endpoint and saves it as CSV.
    """
    if extract_type == 'url':
        df = pd.read_csv(call)
        df.to_csv(save_path, index=False)
    elif extract_type == 'api':
        response = requests.get(call)
        response.raise_for_status() # raise error for bad responses
        df = pd.json_normalize(response.json())
        df.to_csv(save_path, index=False)
    else:
        raise ValueError("Invalid extract_type. Must be 'url' or 'api'.")
