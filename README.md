# 🛒 E-Commerce Website Traffic Analysis — Data Science Project

> **Team 1 | Data Science Project | Python & Jupyter Notebook**

---

## 📌 Project Overview

This project performs a comprehensive **Data Science analysis on E-Commerce Website Traffic data for India**. It covers the full data science pipeline — from data cleaning to visualization — to uncover insights about **peak visit times, user behavior, and conversion trends** across Indian states.

---

## 👥 Team Members

- Ankit
- Samir
- Sushant
- Mahesh
- Pooja

---

## 🛠️ Technologies Used

| Category | Tools / Libraries |
|----------|------------------|
| **Language** | Python 3 |
| **Notebook Environment** | Jupyter Notebook |
| **Data Handling** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn, Plotly Express |
| **Data Source** | `Ecommerce_Website_Traffic_India_more_data.xlsx` |

---

## 📂 Dataset

| Field | Detail |
|-------|--------|
| **File** | `Ecommerce_Website_Traffic_India_more_data.xlsx` |
| **Scope** | Indian E-Commerce Website Traffic |
| **Key Columns** | `user_id`, `date`, `time`, `state`, `age`, `gender`, `device_type`, `page_views`, `session_duration`, `revenue`, `traffic_source` |

---

## 🧹 Data Cleaning Steps

- Removed duplicate rows
- Handled missing values — dropped rows with missing `user_id` and `time`
- Filled missing numeric values with **mean**
- Filled missing categorical values with **mode**
- Fixed case inconsistency (e.g. `Delhi → delhi`)
- Removed trailing/extra spaces
- Fixed invalid negative numeric values
- Handled outliers using **IQR Method**
- Corrected data types (`page_views` → int, `revenue` → float, `date` → datetime)
- Range & value validation (e.g. valid device types: mobile, desktop, tablet)

---

## 📊 Problem Statements & Analysis

### Problem Statement 1 — Peak Visit Times
> *Analyze website traffic data to identify peak visit times*

| Sub-Analysis | Chart Type |
|---|---|
| a) Which states are visited at which time? | Grouped Bar Chart |
| b) Age category visiting at which time slots? | Pivot / Bar Chart |
| d) Total Average Time on Website | Summary Chart |

---

### Problem Statement 2 — User Behavior
> *Understand how users interact with the website*

| Sub-Analysis | Chart Type |
|---|---|
| a) Traffic Source vs Total Purchases | Bar Chart |
| b) Add to Cart vs Purchases | Comparison Chart |
| c) Number of People Visiting by Device | Bar / Pie Chart |
| d) Top 10 States by Purchases | Bar Chart |

---

### Problem Statement 3 — Conversion Trends
> *Identify how traffic converts into sales*

| Sub-Analysis | Chart Type |
|---|---|
| a) Festival vs Purchase Trend | Line / Bar Chart |
| b) State vs Product Purchase | Heatmap |
| c) Monthly Highest & Lowest Sales | Bar Chart |
| d) Total Number of Sold Products | Summary |
| d) User Purchasing Capacity (State Wise) | Boxplot |
| e) Conversion Trends | Line Plot |
| f) Festival with Highest & Lowest Sales | Bar Chart |
| h) Age Group vs Product Search | 2D Histogram |
| i) Gender-wise Traffic Count & Percentage | Pie / Bar Chart |
| j) Gender Percentage by State | Heatmap |

---

## 🚀 How to Run

1. Make sure **Python 3** is installed.
2. Install required libraries:
   ```bash
   pip install pandas numpy seaborn matplotlib plotly openpyxl
   ```
3. Place `Ecommerce_Website_Traffic_India_more_data.xlsx` in the same folder as the notebook.
4. Open the notebook:
   ```bash
   jupyter notebook DATA_SCIENCE_PROJECT_Ecommerce_Website_Traffic_india.ipynb
   ```
5. Run all cells from top to bottom (`Kernel → Restart & Run All`).

---

## 📊 Key Outputs

- State-wise visit patterns by time slot (Morning / Afternoon / Evening / Night)
- Age group behavior and device usage breakdown
- Traffic source effectiveness and purchase conversion
- Top 10 purchasing states in India
- Festival impact on sales trends
- Gender-wise traffic analysis by state
- Monthly sales highs and lows
- Conversion rate trend over time

---

## 📅 Project Info

| Field | Detail |
|-------|--------|
| **Project Type** | Academic Data Science Project |
| **Language** | Python 3 |
| **Notebook Format** | `.ipynb` (Jupyter Notebook) |
| **Domain** | E-Commerce & Web Analytics |
| **Region** | India |

---

## 📝 License

This project is created for **educational purposes only**. All data used is for academic demonstration and analysis.
