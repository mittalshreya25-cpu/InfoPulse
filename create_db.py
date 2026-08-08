import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='shreya__2517@', host='127.0.0.1', port='5432')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'newsdb'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute('CREATE DATABASE newsdb')
        print('Database newsdb created successfully!')
    else:
        print('Database newsdb already exists.')
    cursor.close()
    conn.close()
except Exception as e:
    print(f'Error: {e}')
