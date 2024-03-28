from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from datetime import datetime, timezone


load_dotenv()


host = 'us-east-1-1.aws.cloud2.influxdata.com'
org = "Digital Web"
token = "dOpvhcI-6RsHm3k_P7nwHeQL09XWyQ-dRk4jaJOzNKFCuBFhxLeGWAFPQ7tV4F0kVYOewZpUdlGRib2nvCETUQ=="
bucket = "Database" 

# Initialisez le client InfluxDB
client = InfluxDBClient(url=f"https://{host}", token=token, org=org)

# Créez un point de données en utilisant un objet datetime conscient du fuseau horaire
point = Point("measurement_name").tag("tag_key", "tag_value").field("field_key", 1.23).time(datetime.now(timezone.utc))

# Obtenez l'API d'écriture et écrivez le point dans la base de données
write_api = client.write_api()
write_api.write(bucket=bucket, record=point)

# Utilisez l'API de requête pour interroger les données
query = f'from(bucket:"{bucket}") |> range(start: -1h)'
result = client.query_api().query(query=query, org=org)

# Affichez les résultats
for table in result:
    for record in table.records:
        # Ici, vous pouvez accéder à différentes propriétés de chaque record
        print(f'Temps: {record.get_time()}, Mesure: {record.get_measurement()}, Valeurs: {record.get_value()}')
        # Pour afficher toutes les valeurs et tags sous forme de dictionnaire :
        print(f'Valeurs et tags: {record.values}')
        # Pour afficher des tags spécifiques, par exemple 'tag_key':
        if 'tag_key' in record.values:
            print(f'Tag spécifique - tag_key: {record.values["tag_key"]}')

        print(record.values)

# N'oubliez pas de fermer le client
client.close()
# import os
# import time
# from influxdb_client_3 import InfluxDBClient3, Point
# from dotenv import load_dotenv

# load_dotenv()


# host = os.getenv("INFLUXDB_URL")
# org = os.getenv("INFLUXDB_ORG")
# token = os.getenv("INFLUXDB_TOKEN")
# bucket = os.getenv("INFLUXDB_BUCKET")

# client = InfluxDBClient3(host=host, token=token, org=org)

# database = "Database"

# data = {
#   "point1": {
#     "location": "Klamath",
#     "species": "bees",
#     "count": 23,
#   },
#   "point2": {
#     "location": "Portland",
#     "species": "ants",
#     "count": 30,
#   },
#   "point3": {
#     "location": "Klamath",
#     "species": "bees",
#     "count": 28,
#   },
#   "point4": {
#     "location": "Portland",
#     "species": "ants",
#     "count": 32,
#   },
#   "point5": {
#     "location": "Klamath",
#     "species": "bees",
#     "count": 29,
#   },
#   "point6": {
#     "location": "Portland",
#     "species": "ants",
#     "count": 40,
#   },
# }

# for key in data:
#   point = (
#     Point("census")
#     .tag("location", data[key]["location"])
#     .field(data[key]["species"], data[key]["count"]))
#   client.write(database=database, record=point).time.sleep(1)

# print("Complete. Return to the InfluxDB UI.")

# query = """SELECT *
# FROM 'census'
# WHERE time >= now() - interval '24 hours'
# AND ('bees' IS NOT NULL OR 'ants' IS NOT NULL)"""

# # Execute the query
# table = client.query(query=query, database="Database", language='sql')

# # Convert to dataframe
# df = table.to_pandas().sort_values(by="time")
# print(df)


# query = """SELECT mean(count)
# FROM "census"
# WHERE time > now() - 10m"""

# # Execute the query
# table = client.query(query=query, database="Database", language="influxql")

# # Convert to dataframe
# df = table.to_pandas().sort_values(by="time")
# print(df)

