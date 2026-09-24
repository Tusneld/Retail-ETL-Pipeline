from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

def run_pipeline():
    print('Pipeline Started')

    features_df, sales_df, store_df = extract_data()
    fact_sales, dim_store, dim_date, dim_features = transform_data(features_df,sales_df,store_df)
    load_data(fact_sales, dim_store, dim_date, dim_features)

    print('Pipeline completed, Data loaded to postges successcully')

if __name__ == '__main__':
    run_pipeline()