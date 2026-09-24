import pandas as pd

def extract_data():

    features_def = pd.read_csv(r'C:\Users\USER\Retail-ETL-Pipeline\data\Features_dataset.csv')
    sales_def = pd.read_csv(r'C:\Users\USER\Retail-ETL-Pipeline\data\sales_dataset.csv')                                
    stores_df = pd.read_csv(r'data/stores_dataset.csv')    

    print('Features Dataset') 
    print(features_def.head())
    print(features_def.dtypes)  

    print('Sales Dataset')
    print(sales_def.head())
    print(sales_def.dtypes)

    print('Stores Dataset')
    print(stores_df.head())
    print(stores_df.dtypes)

    return features_def, sales_def, stores_df               