# CS 499 Milestone Four – Database Enhancement Artifact (MongoDB + Dash)

## Overview
This submission demonstrates a database-focused enhancement using MongoDB (Atlas) and a Dash dashboard built on Austin Animal Center (AAC) outcomes data.

## Enhanced Artifact Files
- `ProjectTwoDashboard.ipynb` — Jupyter Notebook that runs the Dash dashboard (port 8050)
- `animal_shelter.py` — MongoDB CRUD module used by the dashboard

## Supporting Files
- `import_aac.py` — script used to import the AAC dataset into MongoDB once MONGO_URI set.
- `aac_shelter_outcomes.csv` — dataset used for import/testing
- `Grazioso_Salavare_Logo.png` — dashboard image asset

## MongoDB Atlas Connection (Environment Variable)
This project expects the MongoDB Atlas connection string to be provided via an environment variable named:

- `MONGO_URI`

Credentials are **not** stored in this repository. Do not hardcode usernames/passwords in code or notebooks.

### Atlas connection string format (example)
```bash
export MONGO_URI="mongodb+srv://<username>:<password>@<cluster-host>/<database>?retryWrites=true&w=majority"

