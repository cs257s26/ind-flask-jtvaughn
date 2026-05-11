"""id,observed_on,quality_grade,latitude,longitude,taxon_id,taxon_name,common_name,iconic_taxon,rank,place_guess,observer,num_id_agreements,url

CREATE TABLE observations (
    id INTEGER PRIMARY KEY,
    observed_on DATE,
    quality_grade TEXT,
    latitude REAL,
    longitude REAL,
    taxon_id INTEGER,
    taxon_name TEXT,
    common_name TEXT,
    iconic_taxon TEXT,
    rank TEXT,
    place_guess TEXT,
    observer TEXT,
    num_id_agreements INTEGER,
    url TEXT
);"""
import pandas as pd
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR  = os.path.join(DATA_DIR, "cleaned")

COLS = ["id", "observed_on", "quality_grade", "latitude", "longitude", "taxon_id", "taxon_name", "common_name", "iconic_taxon", "rank", "place_guess", "observer", "num_id_agreements", "url"]
REQUIRED_COLS = ["id", "observed_on", "latitude", "longitude"]

TAXA = ["amphibians", "birds", "insects", "mammals", "reptiles"]

def clean(csv_file):
    """
    Cleans the data in the given CSV file.

    Parameters:
    csv_file (str): The path to the CSV file to be cleaned.

    Returns:
    pd.DataFrame: A cleaned DataFrame.
    """

    # Select only the columns that match the database schema
    df = pd.read_csv(csv_file)
    df = df[COLS]
    
    # Corerce columns to the correct data types, invalid parsing will be set as NaN
    df["observed_on"] = pd.to_datetime(df["observed_on"], errors='coerce')
    df["id"] = pd.to_numeric(df["id"], errors='coerce')
    df["latitude"] = pd.to_numeric(df["latitude"], errors='coerce')
    df["longitude"] = pd.to_numeric(df["longitude"], errors='coerce')
    
    # Remove rows with missing values in the required columns
    df = df.dropna(subset=REQUIRED_COLS)

    # Remove duplicates based on the 'id' column
    df = df.drop_duplicates(subset=["id"])
    
    # Reset the index after dropping duplicates and missing values
    df=df.reset_index(drop=True)

    return df

def main():
    """
    Main function to clean the data from the CSV file and save it as a new CSV file.
    """
    os.makedirs(OUT_DIR, exist_ok=True)
 
    for taxon in TAXA:
        path = os.path.join(DATA_DIR, f"{taxon}.csv")
        if not os.path.exists(path):
            print(f"{path} not found")
            continue
 
        print(f"[CLEAN] {taxon}.csv ...", end=" ")
        df = clean(path)
 
        out_path = os.path.join(OUT_DIR, f"{taxon}_clean.csv")
        df.to_csv(out_path, index=False)
        print("done")

if __name__ == "__main__":
    main()