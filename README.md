# 📊 Sales Data Analysis: Revenue Drivers & Product Bundling

This project is a Python-based data analysis script designed to clean, analyze, and compare monthly sales data. It specifically compares sales performance between two periods (e.g., August 2019 vs. December 2019) to uncover key revenue drivers, top-performing cities, and frequently bundled products.

## 🚀 Features

The script is divided into three main analytical components:

1. **Robust Data Cleaning (`deep_clean_sales_data`)**
   - Removes empty rows and duplicate entries.
   - Filters out redundant header rows accidentally mixed into the dataset.
   - Standardizes data types (converts quantities and prices to numeric, and dates to datetime objects).

2. **Revenue & Performance Comparison (`analyze_revenue_drivers`)**
   - Calculates and compares **Total Revenue**, **Total Orders**, and **Average Order Value (AOV)** between two months.
   - Calculates percentage growth/decline for key metrics.
   - Automatically deduces *why* revenue changed (e.g., "Customers purchased more products" vs. "Customers purchased higher-priced products").
   - Identifies the **Best-selling** and **Worst-selling** products by total revenue.
   - Extracts city names from raw purchase addresses to rank the **Top 2 Cities by Revenue**.

3. **Market Basket Analysis (`analyze_bundled_products`)**
   - Groups items by `Order ID` to find products purchased together.
   - Uses `itertools` and `collections` to identify and rank the **Top 5 most frequently bought together product pairs**.

## 📁 Project Structure

Ensure your project directory looks like this before running the script:

```text
├── data/
│   ├── sales2019_8.csv    # August sales data
│   └── sales2019_12.csv   # December sales data
├── main.py                # The main Python script
└── README.md              # Project documentation
