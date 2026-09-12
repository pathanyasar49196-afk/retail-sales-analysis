"""
Generates a realistic synthetic Retail Sales dataset for the
End-to-End Retail Sales Analytics project.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N = 5000

regions = ["North", "South", "East", "West", "Central"]
region_weights = [0.22, 0.20, 0.18, 0.22, 0.18]

categories = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Tablet"],
    "Furniture": ["Office Chair", "Study Table", "Sofa", "Bookshelf", "Bed Frame"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Formal Shirt"],
    "Groceries": ["Rice Pack", "Cooking Oil", "Snacks Combo", "Beverages", "Dairy Pack"],
    "Beauty": ["Skincare Kit", "Perfume", "Hair Dryer", "Makeup Kit", "Trimmer"],
}

segments = ["Consumer", "Corporate", "Small Business"]
segment_weights = [0.55, 0.25, 0.20]

ship_modes = ["Standard", "Express", "Same Day"]
ship_weights = [0.6, 0.3, 0.1]

first_names = ["Aarav","Vivaan","Aditya","Ananya","Diya","Ishaan","Kabir","Meera",
               "Neha","Om","Priya","Rohan","Saanvi","Tanvi","Vihaan","Zara",
               "Arjun","Kavya","Rahul","Sneha"]
last_names = ["Sharma","Verma","Iyer","Khan","Patel","Nair","Gupta","Reddy",
              "Singh","Das","Mehta","Joshi","Kapoor","Malhotra","Rao","Chatterjee"]

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for i in range(1, N + 1):
    order_date = start_date + timedelta(days=int(np.random.randint(0, date_range_days)))
    # ship 1-7 days after order
    ship_date = order_date + timedelta(days=int(np.random.randint(1, 8)))

    category = np.random.choice(list(categories.keys()))
    product = np.random.choice(categories[category])

    # base price per category (realistic-ish INR ranges)
    base_price = {
        "Electronics": np.random.randint(2000, 60000),
        "Furniture": np.random.randint(1500, 25000),
        "Clothing": np.random.randint(400, 4000),
        "Groceries": np.random.randint(100, 1500),
        "Beauty": np.random.randint(200, 3000),
    }[category]

    quantity = np.random.randint(1, 6)
    discount = np.random.choice([0, 0.05, 0.10, 0.15, 0.20, 0.25], p=[0.35,0.2,0.2,0.12,0.08,0.05])
    sales = round(base_price * quantity * (1 - discount), 2)

    # profit margin varies by category, with occasional loss-making discounted orders
    margin = {
        "Electronics": 0.12, "Furniture": 0.18, "Clothing": 0.25,
        "Groceries": 0.08, "Beauty": 0.22,
    }[category]
    profit = round(sales * margin - (sales * discount * 0.4), 2)

    customer = f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
    region = np.random.choice(regions, p=region_weights)
    segment = np.random.choice(segments, p=segment_weights)
    ship_mode = np.random.choice(ship_modes, p=ship_weights)

    rows.append({
        "OrderID": f"ORD-{10000+i}",
        "OrderDate": order_date.strftime("%Y-%m-%d"),
        "ShipDate": ship_date.strftime("%Y-%m-%d"),
        "CustomerName": customer,
        "Segment": segment,
        "Region": region,
        "Category": category,
        "Product": product,
        "Quantity": quantity,
        "Discount": discount,
        "Sales": sales,
        "Profit": profit,
        "ShipMode": ship_mode,
    })

df = pd.DataFrame(rows)

# Inject a small amount of realistic messiness for the "data cleaning" step
messy_idx = np.random.choice(df.index, size=60, replace=False)
df.loc[messy_idx[:20], "Discount"] = np.nan
df.loc[messy_idx[20:35], "Region"] = df.loc[messy_idx[20:35], "Region"].str.lower()
df.loc[messy_idx[35:45], "Profit"] = np.nan
dup_rows = df.sample(15, random_state=1)
df = pd.concat([df, dup_rows], ignore_index=True)

df.to_csv("/home/claude/retail-sales-analysis/data/retail_sales_raw.csv", index=False)
print(f"Generated {len(df)} rows -> data/retail_sales_raw.csv")
