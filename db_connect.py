from dotenv import load_dotenv
from influxdb_client_3 import InfluxDBClient3, Point
import datetime
import os

host = "eu.central-1-1.aws.cloud2.influxdata.com"
org = "6a841c0c08328fb1"
token = os.getenv("INFLUXDB_TOKEN")
database = "database"

client = InfluxDBClient3(
    token=token,
    host=host,
    org=org)

data = Point().tag().field().field().time()
client.write(data)

sql = '''SELECT * FROM table'''
table = client.query(query=sql, language='sql', mode='all')
print(table)