import argparse
import os
import pyarrow.parquet as pq
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # download the csv
    csv_name = 'output.parquet'
    os.system(f"wget {url} -O {csv_name}")

    trips = pq.read_table(csv_name)
    trips = trips.to_pandas()


    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    #print(pd.io.sql.get_schema(trips.reset_index(), name='yellow_taxi_data', con=engine))

    print(f"Creating table {table_name} ...")
    trips.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    print(f"Inserting data into table {table_name} ...")
    trips.to_sql(name=table_name, con=engine, if_exists='append')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest parquet data file to postgres')
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='table where to write results')
    parser.add_argument('--url', help='url of datafile')


    args = parser.parse_args()
    main(args)
