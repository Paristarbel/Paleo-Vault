import pandas as pd
import pytest

from queries import (
    get_records_by_year,
    get_records_by_institution,
    get_coordinates_validity,
    get_top_species,
    get_valid_coordinates,
    search_species,
)

CSV_PATH = "clean_fossil_records.csv"


def test_csv_exists_and_loads():
    df = pd.read_csv(CSV_PATH)
    assert df is not None


def test_csv_has_expected_row_count():
    df = pd.read_csv(CSV_PATH)
    assert len(df) == 15070


def test_csv_has_expected_columns():
    df = pd.read_csv(CSV_PATH)
    expected_columns = {
        "scientificName",
        "country",
        "year",
        "basisOfRecord",
        "decimalLatitude",
        "decimalLongitude",
        "institutionCode",
        "collectionCode",
        "datasetName",
        "occurrenceID",
        "media",
        "coordinatesValid",
        "coordinatesInvalid",
    }
    assert expected_columns.issubset(set(df.columns))


def test_coordinates_valid_and_invalid_counts_add_up():
    df = pd.read_csv(CSV_PATH)
    valid_count = df["coordinatesValid"].sum()
    invalid_count = df["coordinatesInvalid"].sum()
    assert valid_count + invalid_count == len(df)


def test_no_duplicate_occurrence_ids_among_non_null():
    df = pd.read_csv(CSV_PATH)
    non_null_ids = df["occurrenceID"].dropna()
    assert len(non_null_ids) == len(non_null_ids.unique())


def test_valid_coordinates_within_south_africa_bounds():
    df = pd.read_csv(CSV_PATH)
    valid_rows = df[(df["coordinatesValid"] == True) & df["decimalLatitude"].notna()]
    assert (valid_rows["decimalLatitude"] >= -35).all()
    assert (valid_rows["decimalLatitude"] <= -22).all()
    assert (valid_rows["decimalLongitude"] >= 16).all()
    assert (valid_rows["decimalLongitude"] <= 33).all()
def test_get_records_by_year_returns_data():
    df = get_records_by_year()
    assert len(df) > 0
    assert "year" in df.columns
    assert "record_count" in df.columns


def test_get_records_by_institution_returns_data():
    df = get_records_by_institution()
    assert len(df) > 0
    assert "institutioncode" in df.columns


def test_get_coordinates_validity_has_two_categories():
    df = get_coordinates_validity()
    assert len(df) == 2


def test_get_top_species_returns_limited_results():
    df = get_top_species()
    assert len(df) <= 10


def test_get_valid_coordinates_within_bounds():
    df = get_valid_coordinates()
    assert (df["decimallatitude"] >= -35).all()
    assert (df["decimallatitude"] <= -22).all()


def test_search_species_finds_known_genus():
    df = search_species("Equus")
    assert len(df) > 0