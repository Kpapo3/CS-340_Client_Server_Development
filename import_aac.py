# Usage:
#
# Set MongoDB Atlas connection string as environment variable.
#   export MONGO_URI="mongodb+srv://<username>:<password>@cluster0.rl4sdmo.mongodb.net/?appName=Cluster0"
#
# Run this script to import CSV into AAC.animals:
#   python import_aac.py
#

import os
import sys
import pandas as pd
from pymongo import MongoClient


DB = "AAC"
COL = "animals"
CSV_FILE = "aac_shelter_outcomes.csv"


def main():
    # Read connection string from environment (do NOT hardcode credentials)
    uri = os.getenv("MONGO_URI")
    if not uri:
        print("ERROR: MONGO_URI environment variable is not set.", file=sys.stderr)
        print('Example: export MONGO_URI="mongodb+srv://user:pass@host/?appName=Cluster0"', file=sys.stderr)
        sys.exit(1)

    # Confirm CSV exists
    if not os.path.exists(CSV_FILE):
        print(f"ERROR: Could not find CSV file: {CSV_FILE}", file=sys.stderr)
        print("Put aac_shelter_outcomes.csv in the same folder as import_aac.py (or update CSV_FILE).", file=sys.stderr)
        sys.exit(1)

    # Load CSV
    df = pd.read_csv(CSV_FILE)

    # Convert numeric field needed for dashboard filtering
    if "age_upon_outcome_in_weeks" in df.columns:
        df["age_upon_outcome_in_weeks"] = pd.to_numeric(df["age_upon_outcome_in_weeks"], errors="coerce")

    # Convert NaN -> None so Mongo stores nulls properly
    df = df.where(pd.notnull(df), None)

    # Connect to Atlas and import
    client = MongoClient(uri)
    col = client[DB][COL]

    # Clear existing docs to avoid duplicates (comment this out if you want to append)
    col.delete_many({})

    records = df.to_dict(orient="records")
    result = col.insert_many(records)

    print(f"Imported {len(result.inserted_ids)} documents into {DB}.{COL}")

    # Quick sanity check
    sample = col.find_one({}, {"_id": 0, "animal_type": 1, "breed": 1, "age_upon_outcome_in_weeks": 1})
    print("Sample document:", sample)


if __name__ == "__main__":
    main()


