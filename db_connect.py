import os
import time
from influxdb_client_3 import InfluxDBClient3, Point
from dotenv import load_dotenv

load_dotenv()


token = os.environ.get("INFLUXDB_TOKEN")
org = "ALP Digital Web"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

client = InfluxDBClient3(host=host, token=token, org=org)

database = "Database"

data = {
  "point1": {
    "location": "Klamath",
    "species": "bees",
    "count": 23,
  },
  "point2": {
    "location": "Portland",
    "species": "ants",
    "count": 30,
  },
  "point3": {
    "location": "Klamath",
    "species": "bees",
    "count": 28,
  },
  "point4": {
    "location": "Portland",
    "species": "ants",
    "count": 32,
  },
  "point5": {
    "location": "Klamath",
    "species": "bees",
    "count": 29,
  },
  "point6": {
    "location": "Portland",
    "species": "ants",
    "count": 40,
  },
}

for key in data:
  point = (
    Point("census")
    .tag("location", data[key]["location"])
    .field(data[key]["species"], data[key]["count"]))
  client.write(database=database, record=point).time.sleep(1)

print("Complete. Return to the InfluxDB UI.")

query = """SELECT *
FROM 'census'
WHERE time >= now() - interval '24 hours'
AND ('bees' IS NOT NULL OR 'ants' IS NOT NULL)"""

# Execute the query
table = client.query(query=query, database="Database", language='sql') )

# Convert to dataframe
df = table.to_pandas().sort_values(by="time")
print(df)


query = """SELECT mean(count)
FROM "census"
WHERE time > now() - 10m"""

# Execute the query
table = client.query(query=query, database="Database", language="influxql")

# Convert to dataframe
df = table.to_pandas().sort_values(by="time")
print(df)

