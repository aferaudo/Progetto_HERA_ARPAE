import urllib.request
import json

# url="https://dati.arpae.it/api/action/datastore_search_sql?sql=SELECT%20LAT,%20LON,%20NETWORK%20from%20%221396fb33-d6a1-442b-a1a1-90ff7a3d3642%22%20GROUP%20BY%20LAT,%20LON,%20NETWORK"
url="https://dati.arpae.it/api/action/datastore_search_sql?sql=SELECT%20data%20from%20%221396fb33-d6a1-442b-a1a1-90ff7a3d3642%22%20LIMIT%202000"

with urllib.request.urlopen(url) as request, open("test.json", "w") as f:
    s = request.read()
    f.write(str(s))
    
    
with open("test.json") as f:
        data = json.load(f)
        print(data)