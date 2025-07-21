import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Setup
sns.set(style="whitegrid")


# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Raheeq',
    database='sales_data'
)

# 1. Monthly Sales Line Chart - last 12 months only
monthly_sales = pd.read_sql("""
SELECT year, month, SUM(gross_sale) AS total_sales
FROM transactions
GROUP BY year, month
ORDER BY year DESC, FIELD(month,
  'January','February','March','April','May','June','July',
  'August','September','October','November','December')
LIMIT 12;
""", conn)

month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']

monthly_sales['month'] = pd.Categorical(monthly_sales['month'], categories=month_order, ordered=True)
monthly_sales = monthly_sales.sort_values(['year', 'month'])

# 2. Yearly Sales Bar Chart
yearly_sales = pd.read_sql("""
SELECT year, SUM(gross_sale) AS total_sales
FROM transactions
GROUP BY year
ORDER BY year;
""", conn)

# 3. Top 5 Customers Pie Chart
top_customers = pd.read_sql("""
SELECT customer_name, SUM(gross_sale) AS total_sales
FROM transactions
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 5;
""", conn)

conn.close()

# Formatter to add commas and disable scientific notation
def thousands_formatter(x, pos):
    return f'{int(x):,}'

# === Plot 1: Monthly Sales Line Chart ===
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_sales, x='month', y='total_sales', hue='year', marker='o')
plt.title('Monthly Gross Sales (Last 12 Months)')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
plt.tight_layout()
plt.show()

# === Plot 2: Yearly Sales Bar Chart ===
plt.figure(figsize=(10, 6))
sns.barplot(data=yearly_sales, x='year', y='total_sales', palette='crest')
plt.title('Yearly Gross Sales')
plt.gca().yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
plt.tight_layout()
plt.show()

# === Plot 3: Top 5 Customers Pie Chart ===
plt.figure(figsize=(8, 8))
plt.pie(top_customers['total_sales'], labels=top_customers['customer_name'], autopct='%1.1f%%', startangle=140)
plt.title('Top 5 Customers by Sales')
plt.tight_layout()
plt.show()
