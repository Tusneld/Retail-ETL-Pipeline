import pandas as pd


def transform_data(features_df, sales_df, store_df):
    # Standardize date fields so downstream joins and date attributes are reliable.
    features_df['Date'] = pd.to_datetime(features_df['Date'])
    sales_df['Date'] = pd.to_datetime(sales_df['Date'], dayfirst= True)

    # Remove markdown columns that are not required by the transformed dataset.
    markdown_colms = ['MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5']
    features_df = features_df.drop(columns = markdown_colms, errors = 'ignore')

    # Build the store dimension from unique source records.
    dim_store = store_df.drop_duplicates().reset_index(drop = True)

    # Create one record per date and holiday combination for the date dimension.
    dim_date = sales_df[['Date', 'IsHoliday']].drop_duplicates().copy()

    # Add calendar attributes used for reporting and time-based analysis.
    dim_date['year'] = dim_date['Date'].dt.year
    dim_date['month'] = dim_date['Date'].dt.month
    dim_date['Week'] = dim_date['Date'].dt.isocalendar().week.astype(int)

    # Build the feature dimension from unique feature records.
    dim_feature = features_df.drop_duplicates().reset_index(drop = True)

    # Preserve the complete sales dataset as the fact table.
    fact_sales = sales_df.copy()

    def normalize(df):
        # Use consistent lowercase column names across all warehouse tables.
        df.columns = df.columns.str.lower()
        return df
    
    # Apply the shared naming convention to every output table.
    dim_date = normalize(dim_date)
    dim_feature = normalize(dim_feature)
    dim_store = normalize(dim_store)
    fact_sales = normalize(fact_sales)

    # Return the fact table followed by the store, date, and feature dimensions.
    return fact_sales, dim_store, dim_date, dim_feature