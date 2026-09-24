import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine


def load_data(fact_sales, dim_store, dim_date, dim_feature):

    db_name = os.getenv('DB_NAME', 'retail_project')
    db_host = os.getenv('DB_HOST', '127.0.0.1')
    db_port = os.getenv('DB_PORT', '5432')
    db_pass = os.getenv('DB_PASSWORD')
    db_user = os.getenv('DB_USER', 'postgres')

    if not db_pass:
        raise RuntimeError('DB_PASSWORD environment variable is required')

    # Safely handle special characters like '@' in the password
    encoded_pass = quote_plus(db_pass)

    engine = create_engine(
        f'postgresql+psycopg2://{db_user}:{encoded_pass}@{db_host}:{db_port}/{db_name}'
    )

    dim_store.to_sql(
        'dim_store', engine, schema='public', if_exists='replace', index=False
    )

    dim_date.to_sql(
        'dim_date', engine, schema='public', if_exists='replace', index=False
    )

    dim_feature.to_sql(
        'dim_feature', engine, schema='public', if_exists='replace', index=False
    )

    fact_sales.to_sql(
        'fact_sales', engine, schema='public', if_exists='replace', index=False
    )

    print('Data loaded to postges successfully')