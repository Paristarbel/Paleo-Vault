import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
import json
import ast

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST")
)
print("Connect successfully!")

df = pd.read_csv("clean_fossil_records.csv")
df['year'] = df['year'].astype('Int64')

print(df.shape)
print(df.columns)

cursor = conn.cursor()

insert_query = """
    INSERT INTO records (
        occurrenceID, scientificName, country, year, basisOfRecord,
        decimalLatitude, decimalLongitude, institutionCode, collectionCode,
        datasetName, media, coordinatesValid, coordinatesInvalid
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

def clean_value(v):
    return None if pd.isna(v) else v

def clean_media(v):
    if pd.isna(v):
        return None
    try:
        parsed = ast.literal_eval(v)
        return json.dumps(parsed)
    except (ValueError, SyntaxError):
        return None

for _, row in df.iterrows():
    cursor.execute(insert_query, (
        clean_value(row['occurrenceID']), clean_value(row['scientificName']),
        clean_value(row['country']), clean_value(row['year']),
        clean_value(row['basisOfRecord']), clean_value(row['decimalLatitude']),
        clean_value(row['decimalLongitude']), clean_value(row['institutionCode']),
        clean_value(row['collectionCode']), clean_value(row['datasetName']),
        clean_media(row['media']), clean_value(row['coordinatesValid']),
        clean_value(row['coordinatesInvalid'])
    ))

conn.commit()
print("All rows inserted successfully!")

cursor.execute("SELECT COUNT(*) FROM records;")
count = cursor.fetchone()[0]
print(f"Total rows in database: {count}")