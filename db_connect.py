from dotenv import load_dotenv
from influxdb_client_3 import InfluxDBClient3, Point
import datetime
import os

load_dotenv()

host = os.getenv("INFLUXDB_HOST")
org = os.getenv("INFLUXDB_ORG")
token = os.getenv("INFLUXDB_TOKEN")
database = "database"

client = InfluxDBClient3(
    token=token,
    host=f"https://{host}",
    org=org)

point = Point("measurement_name").tag("tag_key", "tag_value").field(
    "field_key", "field_value").time(datetime.datetime.utcnow())

write_api = client._write_api
write_api.write(bucket=database, record=point)

query = 'from(bucket:"database") |> range(start: -1h)'
tables = client.query_api().query(query, org=org)
for table in tables:
    for row in table.records:
        print(row.values)
