import requests
import json
import time

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
count=0
while isrequesting_pages:

    try:
        response = requests.get(url,params = params)

        if response.status_code != 200:
            print("Request failed:", response.status_code)
            time.sleep(5)
            continue
    except requests.exceptions.RequestException as error:
        print("Request error: ",error)
        time.sleep(5)
        continue
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
            "occurrenceID":record.get("occurrenceID"),
            "media": record.get("media")}
        clean_records.append(cleaning_record)
    
    if data["endOfRecords"]==True:
        isrequesting_pages=False
        print("All the records have been accessed...")
    else:
       params["offset"] += params["limit"]

    # missing_scienfic_name=sum(1 for infor in clean_records if not infor["scientificName"])
    # missing_latitude=sum(1 for infor in clean_records if infor["decimalLatitude"] is None)
    # missing_longitude=sum(1 for infor in clean_records if infor["decimalLongitude"] is None)
    # missing_year=sum(1 for infor in clean_records if infor["year"] is None)
    # missing_occurence_id=sum(1 for infor in clean_records if not infor["occurrenceID"])
    # media=sum(1 for infor in clean_records if  infor["media"] != [])
    # missing_media=sum(1 for infor in clean_records if not infor["media"])
    # # print("Total records:", len(clean_records))
    # # print(f"Missing scienfic name: {missing_scienfic_name} ")
    # # print(f"Missing latitude: {missing_latitude} ")
    # # print(f"Missing longitude: {missing_longitude} ")
    # # print(f"Missing year: {missing_year} ")
    # # print(f"Missing Occurence-id: {missing_occurence_id} ")
    # # print(f"Records with media:  {media}")
    # # print(f"Records without media:  {missing_media}")

    # missing_scientific_names=[record for record in clean_records if not record["scientificName"]]
    # print("Records missing scientific name : ", len(missing_scientific_names))

    # for record in missing_scientific_names[:10]:
    #     print(record)

    # missing_occurence_ids =[record for record in clean_records if not record["occurrenceID"]]
    # print("Records missing occurence ids : ", len(missing_occurence_ids))

    # for record in missing_occurence_ids[:10]:
    #     print(record)

   

    

