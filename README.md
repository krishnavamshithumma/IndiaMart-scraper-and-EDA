# IndiaMART Scraper and EDA Project

This project involves scraping supplier data from IndiaMART for specific product categories and performing exploratory data analysis (EDA) to uncover insights about supplier behavior, category trends, and geography-based distribution.

---

## 📚 Project Structure

```
.
├── data_collection/
│   ├── queries.json
│   └── scrape.py
├── EDA/
│   └── analysis.py
├── visualizations/
│   ├── Screenshot from 2025-06-02 23-27-05.png
│   ├── Screenshot from 2025-06-02 23-27-29.png
│   ├── Screenshot from 2025-06-02 23-27-51.png
│   ├── Screenshot from 2025-06-02 23-28-49.png
│   └── Screenshot from 2025-06-02 23-29-09.png
└── README.md
```

---

## 🔄 How to Run the Project

### Step 1: Add Keywords

Add the categories/keywords you want to scrape into the `queries.json` file inside the `data_collection/` directory.

### Step 2: Scrape the Data

```
cd data_collection/
```

Then:

1. Log into [IndiaMART](https://www.indiamart.com/) in your browser.
2. Copy your **authorization token** from the network requests.
3. Paste it into the `scrape.py` file:

```python
COMMON_PARAMS = {
    "options.filters.mcategoryid": 178720,
    "options.filters.categoryid": 826,
    "glusrid": 189916653,
    "source": "dir.search",
    "geo_country_info.geo_country_name": "India",
    "geo_country_info.geo_country_code": "IN",
    "implicit_info.for_country.type": "India",
    "implicit_info.for_country.data": "IN",
    # Change this authorization token as per your account
    "AK" : "paste your auth token here"
}
```

Then run:

```
python scrape.py
```

This will scrape data and store it in a SQLite database.

### Step 3: Run EDA

```
cd ../EDA/
```

(Optional) Uncomment the plot code in `analysis.py` if you want to generate visualizations.

```
python analysis.py
```

---

## 📊 EDA Insights

### 1. 🌍 Top States by Number of Suppliers

* **Gujarat, Maharashtra, and Delhi** dominate supplier counts.
* Likely due to industrial ecosystems, ease of doing business, and logistics hubs.

### 2. 🔬 Supplier Ratings per Query Category

* Ratings across categories like **Electronics, Textiles, and Engines** are high (4.3–4.6 median).
* Electronics show more low-end outliers indicating quality variance.

### 3. ⏱️ Supplier Join Year Trend

* Supplier signups peaked in **2015–2017**.
* Sharp drop post-2020 likely due to **COVID disruptions**.

### 4. 📆 Unique Companies per Product Query

* Categories like **Textiles** and **Electronics** have 45+ unique suppliers.
* Indicates a **highly fragmented supplier base** and competitive market.

### 5. 📍 Top Cities with Most Suppliers

* **Delhi, Mumbai, Surat** lead in supplier count.
* Cities like **Rajkot, Jaipur, and Ahmedabad** also show strong presence due to local manufacturing hubs.

### 6. 🔹 Top Queried Categories

| Category                 | Count |
| ------------------------ | ----- |
| Automobile Electronics   | 50    |
| Fabric                   | 26    |
| Diesel Engine            | 22    |
| Other Textile Fabrics    | 17    |
| Cotton Textile           | 11    |
| Four Stroke Engine       | 7     |
| Kirloskar Diesel Engines | 7     |
| Car Petrol Engine        | 6     |
| Portable Petrol Engine   | 4     |
| Car Diesel Engine Parts  | 4     |

These top 10 categories represent the most frequently searched segments and reflect strong demand in **automobile, engine, and textile sectors**.

---

## 🌐 Visualizations

The following visualizations are generated as part of the EDA and are available in the `visualizations/` directory:

### 📊 Top States by Supplier Count
![Top States by Supplier Count](visualizations/Screenshot%20from%202025-06-02%2023-27-05.png)

---

### 📉 Supplier Ratings Boxplot by Category
![Supplier Ratings Boxplot by Category](visualizations/Screenshot%20from%202025-06-02%2023-27-29.png)

---

### 📆 Supplier Join Year Histogram
![Supplier Join Year Histogram](visualizations/Screenshot%20from%202025-06-02%2023-27-51.png)

---

### 🏢 Unique Companies per Product Query
![Unique Companies per Product Query](visualizations/Screenshot%20from%202025-06-02%2023-28-49.png)

---

### 🏙️ Top Cities with Most Suppliers
![Top Cities with Most Suppliers](visualizations/Screenshot%20from%202025-06-02%2023-29-09.png)

---

## 📊 Future Work

* Add time-series trends of product demand.
* Integrate price and MOQ metrics.
* Build dashboards using Streamlit or Dash for interactive filtering.

---

For any issues or contributions, please raise a GitHub issue or open a PR.

---

**Happy Scraping & Analyzing! ✨**
