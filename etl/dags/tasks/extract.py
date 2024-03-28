import requests
import os
import gzip
import shutil

def extract(source, calls, save_dir, replace=False):
    """
    Downloads data from specified URLs and saves it to a given directory. Can handle multiple URLs.
    Skips download if file already exists, unless replace is True.
    Handles different file types appropriately (.gz for decompression, others are saved directly).

    :param source: 'url' for direct downloads or 'api' for API calls (to be implemented).
    :param calls: A list of URLs to download the data from or a single URL string.
    :param save_dir: The local directory path to save the downloaded data.
    :param replace: If True, existing files will be replaced. If False, downloads are skipped if the file exists.
    """
    
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Normalize calls to a list
    if isinstance(calls, str):
        calls = [calls]
    
    for url in calls:
        if source == 'url':
            file_name = os.path.basename(url).replace('.gz', '')  # Extract file name and remove .gz if present
            final_save_path = os.path.join(save_dir, file_name)
            
            # Skip download if the file exists and replace is False
            if os.path.exists(final_save_path) and not replace:
                print(f"File already exists and won't be replaced: {final_save_path}")
                continue
            
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                tmp_file_path = os.path.join(save_dir, os.path.basename(url))
                
                # Save content to a temporary file
                with open(tmp_file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                
                # Decompress if necessary
                if tmp_file_path.endswith('.gz'):
                    with gzip.open(tmp_file_path, 'rb') as f_in:
                        with open(final_save_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    # Clean up the temporary GZip file
                    os.remove(tmp_file_path)
                
                print(f"Data successfully downloaded to {final_save_path}")
            else:
                print(f"Failed to download data. Status code: {response.status_code}")
        elif source == 'api':
            # Placeholder for API extraction logic
            pass
        else:
            raise ValueError("source must be either 'url' or 'api'")


if __name__ == "__main__":
    # Test url
    extract(
        'url'
        #, 'https://cadastre.data.gouv.fr/data/etalab-cadastre/2024-01-01/geojson/departements/13/cadastre-13-parcelles.json.gz'
        , [
            "https://www.data.gouv.fr/fr/datasets/r/78348f03-a11c-4a6b-b8db-2acf4fee81b1" # 2023
            , "https://www.data.gouv.fr/fr/datasets/r/87038926-fb31-4959-b2ae-7a24321c599a" # 2022
            , "https://www.data.gouv.fr/fr/datasets/r/817204ac-2202-4b4a-98e7-4184d154d98c" # 2021
            , "https://www.data.gouv.fr/fr/datasets/r/90a98de0-f562-4328-aa16-fe0dd1dca60f" # 2020
            , "https://www.data.gouv.fr/fr/datasets/r/3004168d-bec4-44d9-a781-ef16f41856a2" # 2019
            , "https://www.data.gouv.fr/fr/datasets/r/1be77ca5-dc1b-4e50-af2b-0240147e0346" # 2018 s2
        ]
        ,'C:/Users/compt/Desktop/de_code/offmarket_re/data/raw/'
    )
    # Test api
    # extract('api', '', 'C:/Users/compt/Desktop/de_code/offmarket_re/data/raw/dvf-13.json')
    