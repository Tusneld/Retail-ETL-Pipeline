# Retail ETL Pipeline

A Python-based Extract, Transform, Load (ETL) pipeline that processes retail sales data from CSV files and loads a dimensional warehouse model into PostgreSQL.

The pipeline extracts features, sales, and store datasets; standardizes and transforms the data; then loads four tables into a PostgreSQL database.

## Features

- Reads retail data from CSV files using pandas
- Converts source date values into consistent datetime values
- Removes unused markdown columns from the feature dataset
- Creates store, date, and feature dimensions
- Preserves sales transactions as a fact table
- Normalizes output column names to lowercase
- Loads transformed data into PostgreSQL using SQLAlchemy
- Replaces destination tables on each pipeline run

## Architecture

```text
CSV files
   |
   v
Extract -> Transform -> Load
                          |
                          v
                 PostgreSQL warehouse
```

## Data Model

The pipeline creates the following tables in the `public` PostgreSQL schema:

| Table | Description |
| --- | --- |
| `dim_store` | Unique store records, including store type and size |
| `dim_date` | Unique sales dates with holiday, year, month, and ISO week attributes |
| `dim_feature` | Unique store and date feature records, excluding markdown columns |
| `fact_sales` | Sales transactions with store, department, date, sales, and holiday data |

Each table is written with `if_exists='replace'`, so an existing table is replaced during every successful run.

## Project Structure

```text
Retail-ETL-Pipeline/
├── data/
│   ├── Features_dataset.csv
│   ├── sales_dataset.csv
│   └── stores_dataset.csv
├── etl/
│   ├── extract.py
│   ├── load.py
│   └── transform.py
├── main.py
└── README.md
```

## Requirements

- Python 3.10 or newer
- PostgreSQL 18 or a compatible PostgreSQL version
- A PostgreSQL database named `retail_project`
- PostgreSQL credentials with permission to create and replace tables

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Tusneld/Retail-ETL-Pipeline.git
cd Retail-ETL-Pipeline
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install pandas sqlalchemy psycopg2-binary
```

## PostgreSQL Setup

Create the target database before running the pipeline:

```sql
CREATE DATABASE retail_project;
```

You can execute this from `psql` or pgAdmin. On a default Windows PostgreSQL installation, `psql.exe` is commonly located at:

```text
C:\Program Files\PostgreSQL\18\bin\psql.exe
```

If `psql` is not recognized in PowerShell, either add that directory to your `PATH` or run the executable with its full path.

## Database Configuration

The current loader connects using these settings:

| Setting | Value |
| --- | --- |
| Host | `127.0.0.1` |
| Port | `5432` |
| Database | `retail_project` |
| Schema | `public` |
| User | `postgres` |

The loader reads these values from environment variables. Keep the real password out of source code and do not commit it to GitHub.

For example, PowerShell environment variables can be defined as follows:

```powershell
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "5432"
$env:DB_NAME = "retail_project"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "your-password"
```

You can copy `.env.example` as a reference, but the application currently reads environment variables directly and does not load a `.env` file automatically.

## Running the Pipeline

Run the pipeline from the repository root:

```powershell
.\.venv\Scripts\python.exe .\main.py
```

Or, with the virtual environment activated:

```bash
python main.py
```

A successful run prints the source dataset previews, followed by completion messages from the load process.

## Verifying the Load

Connect to PostgreSQL and list the tables:

```sql
\c retail_project
\dt public.*
```

You should see:

```text
public.dim_store
public.dim_date
public.dim_feature
public.fact_sales
```

You can also check row counts:

```sql
SELECT 'dim_store' AS table_name, COUNT(*) AS row_count FROM public.dim_store
UNION ALL
SELECT 'dim_date', COUNT(*) FROM public.dim_date
UNION ALL
SELECT 'dim_feature', COUNT(*) FROM public.dim_feature
UNION ALL
SELECT 'fact_sales', COUNT(*) FROM public.fact_sales;
```

## ETL Workflow

### Extract

`etl/extract.py` reads the three source CSV files and prints sample records and data types for inspection.

### Transform

`etl/transform.py`:

1. Converts feature and sales dates to datetime values.
2. Removes the markdown columns from the features dataset.
3. Creates unique store, date, and feature dimensions.
4. Adds year, month, and ISO week attributes to the date dimension.
5. Copies the sales dataset into the sales fact table.
6. Converts all output column names to lowercase.

### Load

`etl/load.py` creates a SQLAlchemy PostgreSQL engine and writes the four transformed DataFrames to the `public` schema.

## Troubleshooting

### `psql` is not recognized

The PostgreSQL command-line client is installed separately from the Python PostgreSQL driver. Add the PostgreSQL `bin` directory to `PATH`, reopen PowerShell, or use the full path to `psql.exe`.

### Database connection errors

Confirm that:

- The PostgreSQL service is running.
- The `retail_project` database exists.
- Host and port match the PostgreSQL server.
- The configured user and password are valid.
- The user can create and replace tables in the `public` schema.

### CSV file not found

Run the pipeline from the repository root. The current extractor uses absolute paths for two datasets and a relative path for `data/stores_dataset.csv`. If the repository is moved to another computer, update those paths or convert the extractor to use paths relative to the project directory.

### Only one table appears in PostgreSQL

Refresh the database schema in pgAdmin and confirm that you are viewing the `retail_project` database and the `public` schema. The loader should create `dim_store`, `dim_date`, `dim_feature`, and `fact_sales`.

## Future Improvements

- Add a configuration library such as `python-dotenv` if automatic `.env` loading is needed
- Replace hardcoded CSV paths with project-relative paths
- Add primary and foreign key constraints to the warehouse tables
- Add logging instead of print statements
- Add automated data-quality checks and tests
- Add incremental loading instead of replacing complete tables
- Add a dependency lock file such as `requirements.txt`

## License

No license has been added yet. Add a license before accepting external contributions or distributing this project publicly.
