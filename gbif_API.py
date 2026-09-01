import requests
import json

all_records=[]
clean_records=[]
isrequesting_pages=True
url="https://api.gbif.org/v1/occurrence/search"

params={"country":"ZA",
        "basisOfRecord":"FOSSIL_SPECIMEN",
        "limit":20 ,
        "offset":0
        }

params["offset"]=0
params["limit"]=300




while isrequesting_pages:

    response=requests.get(url,params=params)
    data=response.json()
    all_records.extend(data["results"])
    records=data["results"]

    for record in data["results"]:

        cleaning_record={"scientificName":record.get("scientificName"),
            "country":record.get("country"),
            "year":record.get("year"),
            "basisOfRecord":record.get("basisOfRecord"),
            "decimalLatitude":record.get("decimalLatitude"),
            "decimalLongitude":record.get("decimalLongitude"),
            "institutionCode":record.get("institutionCode"),
            "collectionCode":record.get("collectionCode"),
            "datasetName":record.get("datasetName"),
            "occurrenceID":record.get("occurrenceID")}
        clean_records.append(cleaning_record)
    
    

    if data["endOfRecords"]==True:
        isrequesting_pages=False
        print("All the records have been accessed...")
    else:
       params["offset"] += params["limit"]




    print(record.get("country"))
    

   