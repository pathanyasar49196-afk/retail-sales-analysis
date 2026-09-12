# Power BI Dashboard Guide — Retail Sales Analytics

This project's Power BI dashboard should be built on `data/retail_sales_clean.csv`
(the cleaned output from the notebook). Steps and DAX measures below.

## 1. Load & Model
1. Open Power BI Desktop → **Get Data → Text/CSV** → select `data/retail_sales_clean.csv`.
2. In Power Query Editor, confirm data types:
   - `OrderDate`, `ShipDate` → Date
   - `Sales`, `Profit`, `ProfitMargin` → Decimal Number
   - `Discount` → Decimal Number (Percentage format)
3. Create a **Date table** (Modeling → New Table):
   ```
   DateTable = CALENDAR(MIN(RetailSales[OrderDate]), MAX(RetailSales[OrderDate]))
   ```
   Mark it as a Date Table and relate it to `OrderDate`.

## 2. Core DAX Measures
```DAX
Total Sales = SUM(RetailSales[Sales])

Total Profit = SUM(RetailSales[Profit])

Total Orders = DISTINCTCOUNT(RetailSales[OrderID])

Avg Order Value = DIVIDE([Total Sales], [Total Orders])

Profit Margin % = DIVIDE([Total Profit], [Total Sales])

Sales MoM Growth % =
VAR CurrentMonthSales = [Total Sales]
VAR PrevMonthSales =
    CALCULATE([Total Sales], DATEADD(DateTable[Date], -1, MONTH))
RETURN DIVIDE(CurrentMonthSales - PrevMonthSales, PrevMonthSales)

Sales YTD = TOTALYTD([Total Sales], DateTable[Date])

Sales Prior Year = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DateTable[Date]))

Sales YoY Growth % = DIVIDE([Total Sales] - [Sales Prior Year], [Sales Prior Year])
```

## 3. Recommended Pages
- **Executive Overview:** KPI cards (Total Sales, Profit, Orders, AOV, Margin %),
  monthly sales trend line chart, YoY growth indicator.
- **Category & Product Performance:** Bar chart of Sales/Profit by Category,
  top 10 products table, treemap of Category → Product.
- **Regional Analysis:** Map or bar chart by Region, slicer for Segment.
- **Discount & Margin Risk:** Scatter plot of Discount vs. Profit Margin,
  table filtered to `ProfitMargin < 0` to flag loss-making orders.

## 4. Interactivity
- Add slicers for `Region`, `Category`, `Segment`, and `OrderMonth`.
- Add drill-through from Category page → Product-level detail page.
- Use bookmarks to toggle between "Sales View" and "Profit View."

## 5. Export
Save as `RetailSalesDashboard.pbix` and add a screenshot to `/images/dashboard_preview.png`
for the GitHub README.
