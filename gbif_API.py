import requests

url="https://api.gbif.org/v1/occurrence/search"

params={"country":"ZA",
        "basisOfRecord":"FOSSIL_SPECIMEN",
        "limit":20}

response=requests.get(url,params=params)

print(response.url)
print(response.status_code)