-- =========================================================
-- Retail Sales Analytics — SQL Layer
-- Author: Yasar Khan Sattar Khan Pathan
-- Load data/retail_sales_clean.csv into this table before running.
-- =========================================================

CREATE TABLE RetailSales (
    OrderID        VARCHAR(20) PRIMARY KEY,
    OrderDate      DATE,
    ShipDate       DATE,
    CustomerName   VARCHAR(100),
    Segment        VARCHAR(30),
    Region         VARCHAR(30),
    Category       VARCHAR(30),
    Product        VARCHAR(50),
    Quantity       INT,
    Discount       DECIMAL(4,2),
    Sales          DECIMAL(12,2),
    Profit         DECIMAL(12,2),
    ShipMode       VARCHAR(20),
    ShippingDays   INT,
    OrderMonth     VARCHAR(7),
    ProfitMargin   DECIMAL(6,3)
);

-- ---------------------------------------------------------
-- 1. Total Sales, Profit, Orders, and Overall Margin
-- ---------------------------------------------------------
SELECT
    SUM(Sales)                          AS TotalSales,
    SUM(Profit)                         AS TotalProfit,
    COUNT(DISTINCT OrderID)             AS TotalOrders,
    ROUND(SUM(Sales) / COUNT(DISTINCT OrderID), 2) AS AvgOrderValue,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2)     AS ProfitMarginPct
FROM RetailSales;

-- ---------------------------------------------------------
-- 2. Monthly Sales Trend
-- ---------------------------------------------------------
SELECT
    OrderMonth,
    SUM(Sales)   AS MonthlySales,
    SUM(Profit)  AS MonthlyProfit
FROM RetailSales
GROUP BY OrderMonth
ORDER BY OrderMonth;

-- ---------------------------------------------------------
-- 3. Top 5 Products by Sales
-- ---------------------------------------------------------
SELECT TOP 5
    Product,
    Category,
    SUM(Sales)   AS TotalSales,
    SUM(Quantity) AS UnitsSold
FROM RetailSales
GROUP BY Product, Category
ORDER BY TotalSales DESC;

-- ---------------------------------------------------------
-- 4. Regional Performance with Rank
-- ---------------------------------------------------------
SELECT
    Region,
    SUM(Sales)  AS TotalSales,
    SUM(Profit) AS TotalProfit,
    RANK() OVER (ORDER BY SUM(Sales) DESC) AS SalesRank
FROM RetailSales
GROUP BY Region;

-- ---------------------------------------------------------
-- 5. Month-over-Month Growth (Window Function)
-- ---------------------------------------------------------
WITH MonthlySales AS (
    SELECT OrderMonth, SUM(Sales) AS TotalSales
    FROM RetailSales
    GROUP BY OrderMonth
)
SELECT
    OrderMonth,
    TotalSales,
    LAG(TotalSales) OVER (ORDER BY OrderMonth) AS PrevMonthSales,
    ROUND(
        (TotalSales - LAG(TotalSales) OVER (ORDER BY OrderMonth)) * 100.0
        / NULLIF(LAG(TotalSales) OVER (ORDER BY OrderMonth), 0), 2
    ) AS MoMGrowthPct
FROM MonthlySales
ORDER BY OrderMonth;

-- ---------------------------------------------------------
-- 6. Orders with Negative Profit Margin (Discount Risk)
-- ---------------------------------------------------------
SELECT OrderID, Product, Discount, Sales, Profit, ProfitMargin
FROM RetailSales
WHERE ProfitMargin < 0
ORDER BY ProfitMargin ASC;

-- ---------------------------------------------------------
-- 7. Customer Segment Contribution (View for Power BI)
-- ---------------------------------------------------------
CREATE VIEW vw_SegmentPerformance AS
SELECT
    Segment,
    SUM(Sales)   AS TotalSales,
    SUM(Profit)  AS TotalProfit,
    COUNT(DISTINCT OrderID) AS Orders
FROM RetailSales
GROUP BY Segment;

-- ---------------------------------------------------------
-- 8. Average Shipping Days by Ship Mode
-- ---------------------------------------------------------
SELECT
    ShipMode,
    AVG(ShippingDays) AS AvgShippingDays,
    COUNT(*) AS OrderCount
FROM RetailSales
GROUP BY ShipMode
ORDER BY AvgShippingDays;
