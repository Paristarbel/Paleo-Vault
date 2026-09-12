import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
import json
import requests
load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST")
)

def get_records_by_year():
    query = "SELECT year, COUNT(*) AS record_count FROM records WHERE year IS NOT NULL GROUP BY year ORDER BY year;"
    return pd.read_sql(query, conn)

def get_records_by_institution():
    query = "SELECT institutioncode, COUNT(*) AS records_per_institution FROM records GROUP BY institutioncode ORDER BY records_per_institution DESC;"
    return pd.read_sql(query, conn)

def get_coordinates_validity():
    query = "SELECT coordinatesvalid, COUNT(*) AS record_count FROM records GROUP BY coordinatesvalid ORDER BY coordinatesvalid;"
    return pd.read_sql(query, conn)

def get_top_species():
    query = "SELECT scientificname, COUNT(*) AS top_species_by_record FROM records WHERE scientificname IS NOT NULL AND scientificname != '' GROUP BY scientificname ORDER BY top_species_by_record DESC LIMIT 10;"
    return pd.read_sql(query, conn)

def get_valid_coordinates():
    query = "SELECT scientificname, decimallatitude, decimallongitude FROM records WHERE coordinatesvalid = true AND decimallatitude IS NOT NULL AND decimallongitude IS NOT NULL;"
    return pd.read_sql(query, conn)
def get_species_media(species_name):
    query = """
        SELECT scientificname, media
        FROM records
        WHERE scientificname = %s
          AND media IS NOT NULL
          AND media::text != '[]'
        LIMIT 5;
    """
    return pd.read_sql(query, conn, params=(species_name,))
def search_species(species_name):
    query = """
        SELECT scientificname
        FROM records
        WHERE scientificname ILIKE %s
          AND scientificname IS NOT NULL
          AND scientificname != ''
        GROUP BY scientificname
        ORDER BY scientificname;
    """
    return pd.read_sql(query, conn, params=(f"%{species_name}%",))


def get_species_records(species_name):
    query = """
        SELECT
            occurrenceid,
            scientificname,
            country,
            year,
            institutioncode,
            collectioncode,
            datasetname,
            decimallatitude,
            decimallongitude
        FROM records
        WHERE scientificname = %s;
    """
    return pd.read_sql(query, conn, params=(species_name,))


def get_species_summary(species_name):
    query = """
        SELECT
            COUNT(*) AS record_count,
            COUNT(DISTINCT institutioncode) AS institution_count,
            MIN(year) AS earliest_year,
            MAX(year) AS latest_year
        FROM records
        WHERE scientificname = %s;
    """
    return pd.read_sql(query, conn, params=(species_name,))

import requests

def get_wikipedia_summary(species_name):
    headers = {
        "User-Agent": "PaleoVault-Student-Project/1.0 (contact: nyoniparis37@gmail.com)"
    }

    name_parts = species_name.split(" ")
    full_name = " ".join(name_parts[:2]) if len(name_parts) >= 2 else name_parts[0]

    for attempt_name in [full_name, name_parts[0]]:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{attempt_name.replace(' ', '_')}"
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("extract"):
                    return {
                        "extract": data.get("extract"),
                        "thumbnail": data.get("thumbnail", {}).get("source")
                    }
        except requests.exceptions.RequestException:
            pass

    return None
if __name__ == "__main__":
    print(get_records_by_year().shape)
    print(get_records_by_institution().shape)
    print(get_coordinates_validity().shape)
    print(get_top_species().shape)
print(get_valid_coordinates().shape)