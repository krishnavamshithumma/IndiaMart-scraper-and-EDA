import requests
import json
import sqlite3
import time
from datetime import datetime
from urllib.parse import urlparse

# --- Load Queries from JSON ---
with open("queries.json", "r") as f:
    queries = json.load(f)  # e.g., ["electronics", "textiles", "mobiles"]

# --- Setup SQLite ---
conn = sqlite3.connect("indiamart_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS indiamart_products (
    query TEXT,
    title TEXT,
    companyname TEXT,
    city TEXT,
    state TEXT,
    rating_count INTEGER,
    supplier_rating REAL,
    memberSince TEXT,
    mcatname TEXT,
    isq TEXT,
    price TEXT,
    desktop_title_url TEXT
)
""")
#to handle duplicates
cursor.execute("""
CREATE UNIQUE INDEX IF NOT EXISTS unique_product
ON indiamart_products(title, companyname, desktop_title_url)
""")

conn.commit()

# --- Constants ---
BASE_URL = "https://dir.indiamart.com/api/search.rp"
HEADERS = {"User-Agent": "Mozilla/5.0"}
COMMON_PARAMS = {
    "options.filters.mcategoryid": 178720,
    "options.filters.categoryid": 826,
    "glusrid": 189916653,
    "source": "dir.search",
    "geo_country_info.geo_country_name": "India",
    "geo_country_info.geo_country_code": "IN",
    "implicit_info.for_country.type": "India",
    "implicit_info.for_country.data": "IN",
    #change this auth token as per your account
    "AK": "#paste your auth token here" 
}

def clean_isq(isq_list):
    return "; ".join(isq_list) if isq_list else ""

def transform_date(date_str):
    try:
        return datetime.fromisoformat(date_str).strftime("%Y-%m-%d")
    except:
        return None

# --- Scrape and Store ---
for query in queries:
    page = 1
    print(f"\n🔍 Scraping for query: '{query}'")
    while True:
        params = COMMON_PARAMS.copy()
        params["q"] = query
        params["page"] = page

        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"❌ Failed page {page} for {query}")
            break

        data = response.json()
        results = data.get("results", [])
        if not results:
            break

        for item in results:
            fields = item.get("fields", {})
            row = (
                query,
                fields.get("title"),
                fields.get("companyname"),
                fields.get("city"),
                fields.get("state"),
                int(fields.get("rating_count", 0)) if fields.get("rating_count") else None,
                float(fields.get("supplier_rating", 0.0)) if fields.get("supplier_rating") else None,
                transform_date(fields.get("memberSince")),
                ", ".join(fields.get("mcatname", [])),
                clean_isq(fields.get("isq")),
                fields.get("indiaPriceFormat"),
                fields.get("desktop_title_url")
            )
            cursor.execute("""
                INSERT OR IGNORE INTO indiamart_products (
                    query, title, companyname, city, state,
                    rating_count, supplier_rating, memberSince,
                    mcatname, isq, price, desktop_title_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, row)
        conn.commit()

        print(f"✅ Page {page} complete")
        if not data.get("nextPage"):
            break
        page += 1
        time.sleep(1)

conn.close()
print("\n🎉 All data saved to SQLite DB: 'indiamart_data.db'")
