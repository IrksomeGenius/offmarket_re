import requests
import os
import gzip
import shutil

def extract(url, save_path):
    """
    Downloads data from a specified URL and saves it to a given path.

    :param url: The URL to download the data from.
    :param save_path: The local file path to save the downloaded data.
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        tmp_gzip_path = save_path + '.gz'
        
        # Save gzip content to temp file
        with open(tmp_gzip_path, 'wb') as tmp_gzip:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_gzip.write(chunk)
        
        # Decompress gzip and save the content
        with gzip.open(tmp_gzip_path, 'rb') as f_in:
            with open(save_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                
        # Clean up the temporary GZip file
        os.remove(tmp_gzip_path)
        
        print(f"Data successfully downloaded and decompressed to {save_path}")
    else:
        print(f"Failed to download data. Status code: {response.status_code}")