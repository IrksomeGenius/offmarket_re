import pandas as pd
from sqlalchemy import create_engine

def load_db(data_path, table_name, db_connection_string):
    """
    Loads processed data from CSV into the specified database table.
    """
    engine = create_engine(db_connection_string)
    df = pd.read_csv(data_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
