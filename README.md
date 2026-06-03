# 📊 E-Commerce Sales Intelligence Dashboard

## 🚀 Live Dashboard

🔗 https://ecommerce-sales-intelligence-agvowtat3sf4wqqh9zqxv2.streamlit.app/

---

## 📌 Project Overview

An end-to-end Business Intelligence and Analytics Dashboard built on the **Olist Brazilian E-Commerce Dataset (100K+ Orders)** using:

* Python
* SQL Analytics
* Streamlit
* Plotly
* Customer Segmentation
* Cohort Analysis
* Time-Series Analytics

This project transforms raw transactional e-commerce data into actionable business insights through advanced analytics, KPI monitoring, and interactive dashboard visualizations.

---

## 🎯 Business Objectives

The dashboard was designed to answer key business questions:

* Which states generate the highest revenue and order volume?
* Which customer segments contribute most to revenue?
* How does customer retention change over time?
* Which sellers perform best in terms of revenue and reviews?
* How do logistics and delivery performance affect customer satisfaction?

---

## 📂 Dataset Information

### Dataset

**Olist Brazilian E-Commerce Dataset**

### Scale

* 100K+ Orders
* Multi-table relational dataset
* Customers, Orders, Sellers, Reviews, Payments, Products

### Data Sources

* Orders
* Customers
* Order Items
* Payments
* Sellers
* Reviews
* Product Information

---

## 🛠 Tech Stack

| Category        | Technologies                |
| --------------- | --------------------------- |
| Programming     | Python                      |
| Analytics       | Pandas, NumPy               |
| SQL Analytics   | pandasql                    |
| Visualization   | Plotly, Matplotlib, Seaborn |
| Dashboard       | Streamlit                   |
| Deployment      | Streamlit Community Cloud   |
| Version Control | GitHub                      |

---

## 📈 Dashboard Features

### ✅ KPI Monitoring

* Total Revenue
* Total Orders
* Average Order Value
* Customer Review Score

### ✅ Revenue Trend Analysis

Interactive monthly revenue growth tracking.

### ✅ RFM Customer Segmentation

Customer segmentation using:

* Recency
* Frequency
* Monetary analysis

### ✅ Seller Performance Analytics

Analysis of:

* Top sellers
* Revenue contribution
* Seller quality metrics

### ✅ Geographic Sales Intelligence

State-wise order and delivery analysis.

### ✅ Cohort Retention Analysis

Customer retention tracking across purchase cohorts.

### ✅ Interactive Filtering

Dynamic filtering by year using Streamlit sidebar controls.

---

## 🧠 Advanced Analytics Implemented

### SQL Analytics

* JOIN operations
* Aggregations
* Common Table Expressions (CTEs)
* Window Functions
* RANK()
* NTILE()

### Customer Analytics

* RFM Segmentation
* Cohort Retention Analysis

### Time-Series Analytics

* Revenue trend analysis
* Seasonal decomposition

### Business Intelligence

* KPI engineering
* Seller performance tracking
* Logistics analytics

---

## 📊 Key Business Insights

* Revenue shows strong month-over-month growth trends.
* High-value customer segments contribute disproportionate revenue.
* Delivery delays negatively impact customer reviews.
* Top sellers dominate marketplace revenue contribution.
* Customer retention varies significantly across cohorts.

---



## 📁 Project Structure

```text
ecommerce-sales-intelligence/
│
├── app.py
├── requirements.txt
├── README.md
│
├── olist_master_powerbi.csv
├── rfm_segments.csv
├── state_summary.csv
├── top_sellers.csv
├── cohort_retention.csv
├── monthly_revenue.csv
│
└── images/
```

---

## ⚡ Deployment

The application is deployed on Streamlit Community Cloud.

### Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔮 Future Improvements

* Forecasting using ARIMA/Prophet
* Interactive geographic maps
* Product category filtering
* Customer Lifetime Value (CLV)
* Recommendation system
* Advanced seller ranking engine

---

## 👨‍💻 Author

### Farhan Ansari

M.Tech Data Analytics
Indian Institute of Technology (ISM) Dhanbad

---

## ⭐ If You Found This Project Useful

Please consider giving this repository a star ⭐
