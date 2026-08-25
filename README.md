# 🦴 Paleo_Vault

## A Mini  Fossil & Hominid Data Pipeline for Paleoanthropological Research Data in South Africa 🇿🇦

This is an educational  data engineering project that explores how scientific and paleoanthropological data can be ingested, cleaned, validated ,transformed, stored, and queried.

The project combines my interest in programming, data engineering, and paleoanthropology into one manageable project.

## Project Architecture
                 GBIF / Museum Data
                         │
                         ↓
                  EXTRACT
                Python + API
                         │
                         ↓
                 TRANSFORM
          Pandas + validation
                         │
                         ↓
                    LOAD
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
        PostgreSQL/SQL          Parquet
              │
              ↓
       ┌───────────────┐
       │               │
       ↓               ↓
  SQL Analysis      MAP
       │               │
       ↓               ↓
Species trends   Fossil locations
Site counts      Hominin locations
Time periods     Museum records

## 📊 Data
This project may work with structured and semi-structured datasets containing information such as:

>Specimen ID,
 >Species,
 >Genus,
 >Discovery site,
 >Country,
 >Latitude,
 >Discovery date,
 >Geological age,
 >Researcher,
 >Institution,
 >Publication

## 🛠️ Technology Stack
### Current

>Python,
 >Pandas,
 >PostgreSQL,
 >SQL,
 >Git,
 >GitHub

### Planned Exploration

>CSV, 
 >JSON,
 >Parquet,
 >Docker,
 >REST APIs,
 >Apache Airflow,
 >Apache Kafka,
 >Cloud Storage,
 >Data Quality Testing,
 >Data Warehousing

## 🔄 ETL Pipeline

### Extract 

Collecting data from available datasets and/or public data sources.

### Transform 
Use python and pandas to:
 >Inspect the data, 
 >Handle missing values, 
 >Remove duplicates, 
 >Standardize formats, 
 >Validate values, 
 >Transform columns, 
 >Prepare data for storage

### Load
Load the processed data into PostgreSQL for structured storage and SQL analysis.

## 🗄️ Database Design
The project will use a relational database to represent related entities.

This is the planned module and I will refine the schema as  I develop the project:

 species
    │
    ▼
 specimens ─────── sites
    │
    ▼
 researchers

## 🔍 Example Data Questions

### Paleo_Vault will eventually allow questions such as:

 >How many specimens are associated with each species?, 
 >Which sites contain the most recorded specimens?, 
 >Which countries have the most discoveries?, 
 >Which researchers are associated with specific discoveries?, 
 >How are discoveries distributed across geological periods?,
 >Which records contain missing or invalid information?,
 >Are there duplicate specimen records?


##🧪 Data Quality
PaleoVault will check for:

Missing values, 
 Duplicate records,
 Invalid dates,
 Invalid coordinates,
 Incorrect data types,
 Inconsistent names,
 Invalid relationships between records

Invalid records will be identified and handled deliberately rather than silently discarded.

## 📁 Project Structure

PaleoVault/

│

├── data/

│   ├── raw/

│   └── processed/

│
├── notebooks/

│
├── src/

│   ├── ingestion/

│   ├── transformation/

│   ├── validation/

│   └── loading/

│

├── sql/

│   ├── schema.sql

│   └── queries.sql

│

├── tests/

│

├── .gitignore

├── requirements.txt

└── README.md


## 🚀 Learning Goals

Through PaleoVault, I aim to develop practical experience with:

ETL pipelines
Data ingestion
Data cleaning
Data validation
Relational databases
PostgreSQL
SQL
Data modelling
Data storage
Data quality
Pipeline architecture

The project will provide a foundation for exploring more advanced data engineering concepts such as batch processing, streaming, orchestration, and cloud storage.

## 📈 Development Roadmap
### Version 1 — Basic ETL
CSV → Pandas → PostgreSQL

### Version 2 — Multiple Data Formats
CSV + JSON → ETL → PostgreSQL

### Version 3 — Data Lake + Warehouse
Raw Data → Data Lake → Transformation → Data Warehouse

### Version 4 — Orchestration
Airflow → Pipeline → Data Warehouse

### Version 5 — Streaming
Data Source → Kafka → Processing → Storage

### Version 6 — Scalable Processing
Large Dataset → Spark → Data Warehouse

The project will remain intentionally manageable while each stage introduces a new data engineering concept.

## 🎓 Academic Purpose

PaleoVault is an independent project created to strengthen my practical understanding of data engineering and demonstrate how data engineering concepts can be applied to a scientific domain that I am personally interested in.
