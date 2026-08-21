# 🦴 Paleo_Vault

## A Mini Data Engineering Pipeline for Paleoanthropological Research Data

This is an educational  data engineering project that explores how scientific and paleoanthropological data can be ingested, cleaned, validated ,transformed, stored, and queried.

The project combines my interest in programming, data engineering, and paleoanthropology into one manageable project.

## Project Architecture

        Raw Research Data
               │
               ▼
        Data Ingestion
               │
               ▼
             Pandas
               │
               ▼
    Cleaning & Validation
               │
               ▼
       Transformation
               │
               ▼
          PostgreSQL
               │
               ▼
         SQL Analysis

## 📊 Data
This project may work with structured and semi-structured datasets containing information such as:

>Specimen ID
>Species
>Genus
>Discovery site
>Country
>Latitude
>Longitude
>Discovery date
>Geological age
>Researcher
>Institution
>Publication

## 🛠️ Technology Stack
### Current

>Python
>Pandas
>PostgreSQL
>SQL
>Git
>GitHub

### Planned Exploration

>CSV
>JSON
>Parquet
>Docker
>REST APIs
>Apache Airflow
>Apache Kafka
>Cloud Storage
>Data Quality Testing
>Data Warehousing

## 🔄 ETL Pipeline

### Extract 

Collecting data from available datasets and/or public data sources.

### Transform 
Use python and pandas to:
>Inspect the data
>Handle missing values
>Remove duplicates
>Standardize formats
>Validate values
>Transform columns
>Prepare data for storage

### Load
Load the processed data into PostgreSQL for structured storage and SQL analysis.
