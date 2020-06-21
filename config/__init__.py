import os

from dotenv import load_dotenv

from config.const import *


load_dotenv()

# Using in aiopg.sa
pg_config = {
    'host': os.getenv("DATABASE_HOST"),
    'port': os.getenv("DATABASE_PORT"),
    'user': os.getenv("DATABASE_USERNAME"),
    'password': os.getenv("DATABASE_PASSWORD"),
    'database': os.getenv("DATABASE_NAME")
}

# Using in migrations
sql_conn_url = f"postgresql+psycopg2://{pg_config['user']}:{pg_config['password']}" \
               f"@" \
               f"{pg_config['host']}:{pg_config['port']}/{pg_config['database']}"
