import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Connect to SQLite DB
conn = sqlite3.connect("/home/vamsi/Desktop/slooze_assignment/data_collection/indiamart_data.db")

# Load data
df = pd.read_sql_query("SELECT * FROM indiamart_products", conn)

# Close connection after load
conn.close()


# Data Cleaning & Parsing

df['price'] = df['price'].str.replace('₹', '').str.replace(',', '').str.extract(r'(\d+\.?\d*)').astype(float)
df['memberSince'] = pd.to_datetime(df['memberSince'], errors='coerce')
df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')
df['supplier_rating'] = pd.to_numeric(df['supplier_rating'], errors='coerce')


# Top Categories / Product Types
df['mcatname_list'] = df['mcatname'].fillna('').apply(lambda x: [i.strip() for i in x.split(',') if i.strip()])
all_mcats = pd.Series([item for sublist in df['mcatname_list'] for item in sublist])
top_mcats = all_mcats.value_counts().head(10)
print(f"Top categories : {top_mcats}")


# Regional Supplier Insights
top_states = df['state'].value_counts().head(10)

plt.figure(figsize=(10, 5))
sns.barplot(x=top_states.values, y=top_states.index)
plt.title("Top States by Number of Suppliers")
plt.xlabel("Number of Suppliers")
plt.ylabel("State")
plt.show()


# Rating Analysis
plt.figure(figsize=(10, 6))
sns.boxplot(x='query', y='supplier_rating', data=df)
plt.title("Supplier Ratings per Query Category")
plt.ylabel("Rating (Out of 5)")
plt.xticks(rotation=45)
plt.show()


# Supplier Longevity

df['member_year'] = df['memberSince'].dt.year
member_trend = df['member_year'].value_counts().sort_index()

plt.figure(figsize=(10, 5))
sns.lineplot(x=member_trend.index, y=member_trend.values)
plt.title("Supplier Join Year Trend")
plt.xlabel("Year")
plt.ylabel("Number of Suppliers")
plt.show()


# ISQ Keyword Frequency

df['isq_keywords'] = df['isq'].fillna('').apply(lambda x: re.findall(r'(\w+)==', x))
all_isq_keywords = pd.Series([kw for sublist in df['isq_keywords'] for kw in sublist])
top_isq_keywords = all_isq_keywords.value_counts().head(10)

# plt.figure(figsize=(10, 5))
# sns.barplot(x=top_isq_keywords.values, y=top_isq_keywords.index)
# plt.title("Most Common ISQ (Attribute) Keys")
# plt.xlabel("Frequency")
# plt.ylabel("ISQ Key")
# plt.show()

# Unique companies per query
unique_companies_per_query = df.groupby('query')['companyname'].nunique().sort_values(ascending=False)
print("\nUnique Companies per Query:\n", unique_companies_per_query)

# plt.figure(figsize=(10, 5))
# sns.barplot(x=unique_companies_per_query.index, y=unique_companies_per_query.values)
# plt.title("Unique Companies per Product Query")
# plt.xlabel("Query Keyword")
# plt.ylabel("Unique Companies")
# plt.xticks(rotation=45)
# plt.show()

# Supplier Count per City
suppliers_per_city = df['city'].value_counts().head(15)
print("\nTop Cities by Supplier Count:\n", suppliers_per_city)

# plt.figure(figsize=(10, 6))
# sns.barplot(x=suppliers_per_city.values, y=suppliers_per_city.index)
# plt.title("Top Cities with Most Suppliers")
# plt.xlabel("Number of Suppliers")
# plt.ylabel("City")
# plt.show()

# Number of Products per Company (Top 15)
products_per_company = df['companyname'].value_counts().head(15)
print("\nTop Companies by Number of Products:\n", products_per_company)

# plt.figure(figsize=(10, 6))
# sns.barplot(x=products_per_company.values, y=products_per_company.index)
# plt.title("Top Companies by Number of Products Listed")
# plt.xlabel("Products Listed")
# plt.ylabel("Company Name")
# plt.show()



