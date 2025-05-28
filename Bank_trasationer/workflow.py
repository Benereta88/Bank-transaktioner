from prefect import flow, task
import pandas as pd
from sqlalchemy import create_engine

@task
def import_csv(csv_path, mapped_columns_to_import=None):
    if mapped_columns_to_import is None:
        dataframe = pd.read_csv(csv_path)
    else:
        dataframe = pd.read_csv(csv_path, usecols=mapped_columns_to_import.keys())
    return dataframe

@task
def write_to_postgres(dataframe, table_name, db_url, mapped_columns_to_import=None):
    if mapped_columns_to_import:
        dataframe.rename(columns=mapped_columns_to_import, inplace=True)
    engine = create_engine(db_url)
    dataframe.to_sql(table_name, engine, if_exists='append', index=False, method='multi')

@flow
def load_data_flow():
    mapped_columns_to_import = {
        "transaction_id": "transaction_id",
        "timestamp": "timestamp",
        "amount": "amount",
        "currency": "currency",
        "sender_account": "sender_account",
        "receiver_account": "receiver_account",
        "sender_country": "sender_country",
        "sender_municipality": "sender_municipality",
        "receiver_country": "receiver_country",
        "receiver_municipality": "receiver_municipality",
        "transaction_type": "transaction_type",
        "notes": "notes"
    }
    dataframe = import_csv("transactions.csv", mapped_columns_to_import)
    write_to_postgres(
        dataframe,
        "fun_characters",
        "postgresql://postgres:Pipi-ina-18@localhost:5432/Bank_trasationer",
        mapped_columns_to_import
    )

if __name__ == "__main__":
    load_data_flow()
