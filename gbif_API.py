import requests
import json

# print(response.url)
# print(response.status_code)
# print(len(records))

all_records=[]
isrequesting_pages=True
url="https://api.gbif.org/v1/occurrence/search"

params={"country":"ZA",
        "basisOfRecord":"FOSSIL_SPECIMEN",
        "limit":20 ,
        "offset":0
        }


params["offset"]=0
params["limit"]=300
response=requests.get(url,params=params)
data=response.json()
record=data["results"]
while isrequesting_pages:

    record=data["results"][0]
    response=requests.get(url,params=params)
    data=response.json()
    all_records.extend(data["results"])

    if data["endOfRecords"]==True:
        isrequesting_pages=data["endOfRecords"]
        print("All the records have been accessed...")
    else:
       params["offset"] += params["limit"]
    print(data["results"][0]["occurrenceID"])
    print(record.get("year"))
    print(data["results"][0]["basisOfRecord"])
    print((data["results"][0]).get("decimalLatitude"))

   