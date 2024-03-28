import pandas as pd

def transform(source_path, target_path):
    """
    Reads raw data, transforms it, and saves the processed data.
    """
    df = pd.read_csv(source_path)
    # Example transformation: Drop missing values
    df_clean = df.dropna()
    df_clean.to_csv(target_path, index=False)
