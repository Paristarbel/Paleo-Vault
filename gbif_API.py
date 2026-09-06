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

        print("Requesting offset:", params["offset"], flush=True)

        response = requests.get(url, params=params, timeout=30)

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

        latitude_bad = record.get("decimalLatitude") is not None and (record.get("decimalLatitude") < -35 or record.get("decimalLatitude") > -22)

        longitude_bad = record.get("decimalLongitude") is not None and (record.get("decimalLongitude") < 16 or record.get("decimalLongitude") > 33)

        coordinatesInvalid = latitude_bad or longitude_bad

        coordinatesValid = not coordinatesInvalid

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
            "media": record.get("media") or [],
            "coordinatesValid": coordinatesValid,
            "coordinatesInvalid":coordinatesInvalid}

        clean_records.append(cleaning_record)

    if data["endOfRecords"]==True:

        isrequesting_pages=False

        print("All the records have been accessed...")

    else:

       params["offset"] += params["limit"]


missing_scientific_names=[record for record in clean_records if not record["scientificName"]]

print("Records missing scientific name : ", len(missing_scientific_names))

missing_occurence_ids =[record for record in clean_records if not record["occurrenceID"]]

print("Records missing occurence ids : ", len(missing_occurence_ids))

missing_media = [record for record in clean_records if record["media"] == []]

print("Records with empty media list: ", len(missing_media))

print("Total clean_records:", len(clean_records))


invalidCoordinate_latitude=[record for record in clean_records if (record["decimalLatitude"] is not None ) and (record["decimalLatitude"] < -35 or record["decimalLatitude"] > -22)]

invalidCoordinate_longitude=[record for record in clean_records if (record["decimalLongitude"] is not None ) and (record["decimalLongitude"] < 16 or record["decimalLongitude"] > 33)]

print("Records with invalid latitude: ", len(invalidCoordinate_latitude))

print("Records with invalid longitude: ", len(invalidCoordinate_longitude))

invalid_ids = set(
    r["occurrenceID"]
    for r in invalidCoordinate_latitude
    if r["occurrenceID"] is not None
) & set(
    r["occurrenceID"]
    for r in invalidCoordinate_longitude
    if r["occurrenceID"] is not None
)

print("Records with BOTH invalid latitude and longitude:", len(invalid_ids))

invalid_flagged = [record for record in clean_records if record["coordinatesInvalid"]]

print("Records flagged coordinatesInvalid:", len(invalid_flagged))


Occurrence_isNone=set(
    record["occurrenceID"]
    for record in clean_records
    if record["occurrenceID"] is None
)

print(f"Occurrence IDs missing: {len(Occurrence_isNone)}")

Occurrence_isNotNone=set(
    record["occurrenceID"]
    for record in clean_records
    if record["occurrenceID"] is not None
)

print(f"Occurrence IDs present: {len(Occurrence_isNotNone)}")

Occurrence_hasID_list = [
    record["occurrenceID"]
    for record in clean_records
    if record["occurrenceID"] is not None
]

if len(Occurrence_hasID_list) != len(Occurrence_isNotNone):

    duplicate_count = len(Occurrence_hasID_list) - len(Occurrence_isNotNone)

    print(f"There are {duplicate_count} ID duplicates")

else:

    print("There are no duplicates")
