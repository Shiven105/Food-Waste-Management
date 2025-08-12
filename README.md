# Local Food Wastage Management System

This repository contains a Streamlit application and SQLite database for the Local Food Wastage Management System project.

## What you get
- SQLite DB: `/mnt/data/food_waste.db`
- Cleaned CSVs: `clean_providers.csv`, `clean_receivers.csv`, `clean_food_listings.csv`, `clean_claims.csv`
- Streamlit app: `app_full.py`
- Helper module: `streamlit_helpers.py`
- SQL queries file: `queries.sql`
- SQL explanations: `sql_explanations.md`
- Video script: `video_script.md`

## How to run locally (Linux/Mac/Windows)
1. Install Python 3.9+
2. Create venv (optional): `python -m venv venv` then `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Run the Streamlit app: `streamlit run /mnt/data/app_full.py`
5. Open the URL printed by Streamlit (usually http://localhost:8501)

## Deployment
- To deploy to Streamlit Cloud, push the files to a GitHub repo and connect the repo to Streamlit Cloud. Set `app_full.py` as the main file.

## Note
This app uses a local SQLite DB included in the repository for demo and submission purposes.