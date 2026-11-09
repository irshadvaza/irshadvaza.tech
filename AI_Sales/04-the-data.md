# Chapter 4: The data

> 🎯 **What you will learn**
> - The four tables, what each one means, and what the columns are for
> - What a **star schema** is, and why this project uses one
> - How to look at the data yourself with a few lines of Python
> - The "dirt" hidden in the raw files, which later chapters will clean

⏱️ Time: about 40 minutes. You will run a small Python script.

> ℹ️ **About this data.** The CSV files are **synthetic**: created for learning, not taken from a real company. The shop names, cities and numbers are realistic but invented. That means you can share, publish and experiment freely.

---

## 🧸 A school analogy

Think of a school's records:

| School | Sales AI |
|---|---|
| A **class register**: *who* attended *which lesson* on *which date* | **Sales transactions**: *which product* sold in *which store* on *which date* |
| A **student list** (name, age, class) | **Products** list |
| A **room list** (building, size) | **Stores** list |
| A **school calendar** (holidays, exam weeks) | **Calendar** table (holidays, weather, promotions) |

The register is huge and changes every day. The three lists are small and rarely change. We keep them **separate** so facts are stored once. Imagine writing a student's full address in the register every single day. Wasteful, and easy to get wrong!

---

## 📦 The four files

All files are in the `data/` folder.

```text
data/
├── Initial-Training-Data/        <- the 5-year history used to train the first model
│   ├── products.csv
│   ├── stores.csv
│   ├── calendar_marketing_external.csv
│   └── sales_transactions.csv
└── Jan-March-2026/               <- three new months, used to practise "upload and retrain"
    ├── sales_transactions_2026_01.csv  (+ _02, _03)
    └── calendar_marketing_external_2026_01.csv  (+ _02, _03)
```

| File | Rows | Covers | Changes how often? |
|---|---|---|---|
| `products.csv` | 6 | the catalog | rarely |
| `stores.csv` | 8 | the store network | rarely |
| `calendar_marketing_external.csv` | **1,826** (one per day) | 2021-01-01 to 2025-12-31 | every new period |
| `sales_transactions.csv` | **84,928** | 2021-01-01 to 2025-12-31 | every new period |

The `Jan-March-2026` folder has only sales and calendar files, because products and stores do not change. Each monthly file holds roughly 1,300 to 1,450 sales rows, similar to a normal month in the history.

---

## 1️⃣ Products: *what we sell*

One row per product. There are six, one per category.

| product_id | product_name | category | base_price | lifecycle | demand class | seasonality |
|---|---|---|---|---|---|---|
| P001 | Voltix Smart Watch Pro 300 | Electronics | 12,500 | Growing | Medium Volume | Highly Seasonal |
| P002 | FreshFarm Packaged Foods Essential 400 | Grocery | 180 | Mature | High Volume | Moderately Seasonal |
| P003 | Urbane Women's Classic 700 | Clothing | 1,800 | Mature | Medium Volume | Highly Seasonal |
| P004 | Coolwell Air Conditioner Max 500 | Home Appliances | 38,000 | Mature | Low Volume | Highly Seasonal |
| P005 | Peakform Fitness Equipment Elite 200 | Sports & Fitness | 6,500 | Growing | Medium Volume | Moderately Seasonal |
| P006 | Luvena Skincare Daily 900 | Beauty & Personal Care | 650 | Mature | High Volume | Moderately Seasonal |

The file has **16 columns**. Beyond the ones above it also holds `subcategory`, `brand`, `product_type`, `launch_date`, `cost_price`, `return_rate_baseline`, `trend_annual_multiplier`, `price_elasticity_tier` and `category_seasonality_flavor`.

> 📖 **Price elasticity** means: *if the price goes up a bit, how much does demand fall?* High elasticity = shoppers are very price-sensitive.

## 2️⃣ Stores: *where we sell*

One row per store. Eight stores in eight Indian cities.

| store_id | store_name | type | size (sq ft) | city tier | performance segment |
|---|---|---|---|---|---|
| S01 | Mumbai Flagship 01 | Flagship | 22,000 | 1 | Top Performer |
| S02 | Bengaluru Flagship 02 | Flagship | 19,500 | 1 | Top Performer |
| S03 | Delhi Standard 03 | Standard | 11,000 | 1 | Core Performer |
| S04 | Hyderabad Standard 04 | Standard | 9,800 | 1 | Core Performer |
| S05 | Pune Standard 05 | Standard | 8,600 | 1 | Core Performer |
| S06 | Ahmedabad Compact 06 | Compact | 5,200 | 2 | Core Performer |
| S07 | Lucknow Compact 07 | Compact | 4,400 | 2 | Underperformer |
| S08 | Jaipur Express 08 | Express | 2,600 | 2 | Underperformer |

17 columns in total, including `city`, `state`, `region`, `latitude`, `longitude`, `customer_density` and `average_income_index`. These explain *why* one store sells more than another.

## 3️⃣ Calendar, marketing and external: *what was happening that day*

One row for **every day** (35 columns). It holds the context that moves demand.

| Group | Columns (examples) | Why it matters |
|---|---|---|
| Calendar | `day_of_week`, `month`, `quarter`, `is_weekend`, `is_month_end` | Weekly and monthly shopping habits |
| Holidays | `holiday_flag`, `holiday_name`, `days_to_holiday`, `days_from_holiday` | People shop *before* festivals |
| Promotions | `promotion_event`, `marketing_campaign`, `campaign_intensity` | Sales and discounts boost demand |
| Weather | `temperature_c`, `rainfall_mm`, `humidity_pct`, `weather_condition` | Hot days sell air conditioners |
| Economy | `inflation_index`, `consumer_confidence_index`, `unemployment_rate`, `fuel_price_index` | Spending power |
| Ad spend | `digital_ad_spend`, `offline_ad_spend` | Marketing effort |

A real row (2021-01-01): *Friday, holiday "New Year" (National), 14.4 °C, cold, no promotion.*

## 4️⃣ Sales transactions: *what actually happened*

The **fact table**. One row per sale record (18 columns).

| Column | Meaning |
|---|---|
| `transaction_id` | Unique ID, for example `T000000001` |
| `date`, `product_id`, `store_id` | **When, what and where.** These link to the other three tables |
| `channel_id` | Online, Physical Store, Mobile App or Marketplace |
| `customer_segment_id` | e.g. Value Seeker, Loyal Regular, Premium Buyer |
| `units_sold` | **The number we forecast** (the "target") |
| `unit_price`, `gross_sales`, `discount_amount`, `net_sales` | Money columns |
| `promotion_id`, `discount_percentage` | Was a promotion active? |
| `inventory_available`, `stockout_flag` | Stock on hand, and whether we ran out |
| `return_units`, `return_amount` | Returned goods |
| `true_demand_estimate` | What customers would have bought with unlimited stock |

A real row: *Transaction T000000001 on 2021-01-01: 311 smart watches sold at store S01, through the Physical Store channel.*

---

## ⭐ The star schema

Four tables, one rule: **the sales table sits in the middle and the other three connect only to it.**

![Star schema](../images/diagrams/03-star-schema-er.svg)

How to read the lines:

| Link | Reads as | Linked by |
|---|---|---|
| products → sales | One product appears in **many** sales rows. Each sales row has **exactly one** product. | `product_id` |
| stores → sales | One store has many sales. Each sale happened in one store. | `store_id` |
| calendar → sales | One date has many sales. Each sale has one date. | `date` |

This is called **one-to-many (1:N)**. The three small tables are **dimension tables** ("the descriptions"). The big one is the **fact table** ("the events"). Dimension tables never connect to each other, which is why the picture looks like a star. ⭐

> 🧠 **Key terms**
> - **Primary key (PK):** a column whose value is unique per row, like a passport number.
> - **Foreign key (FK):** a column that *points to* a primary key in another table, like writing a passport number on a hotel form.

**Why a star?** Facts are stored once. Joins are simple. Reports and ML features are easy to build. The Silver notebook ([Chapter 6](06-silver.md)) joins the star back into one wide table.

---

## 🐍 Hands-on: look at the data yourself

Create a file `explore_data.py` anywhere (or use a notebook). From the repo root:

```python
import pandas as pd

D = "data/Initial-Training-Data/"

sales    = pd.read_csv(D + "sales_transactions.csv", parse_dates=["date"])
products = pd.read_csv(D + "products.csv")
stores   = pd.read_csv(D + "stores.csv")
calendar = pd.read_csv(D + "calendar_marketing_external.csv", parse_dates=["date"])

print(sales.shape, products.shape, stores.shape, calendar.shape)
```

Expected output:

```text
(84928, 18) (6, 16) (8, 17) (1826, 35)
```

**Line by line**

| Line | What it does |
|---|---|
| `import pandas as pd` | Loads **pandas**, Python's table library. `pd` is the short nickname. |
| `D = "data/..."` | Saves the folder path in a variable so we type it once. |
| `pd.read_csv(...)` | Reads a CSV into a **DataFrame** (a table in memory). |
| `parse_dates=["date"]` | Turns the text `"2021-01-01"` into a real date. |
| `.shape` | Gives *(rows, columns)*. |

### Join the star into one table

```python
full = (
    sales
    .merge(products, on="product_id", how="left")
    .merge(stores,   on="store_id",   how="left", suffixes=("", "_store"))
    .merge(calendar, on="date",       how="left", suffixes=("", "_cal"))
)
print(full.shape)                       # (84928, 83)
print(len(full) == len(sales))          # True
```

`how="left"` means *keep every sales row and attach the matching description*. Because it is a one-to-many star, **no sales row is lost or duplicated**. That `True` is your proof. Check it every time you join. It is the cheapest data-quality test there is.

### A first business question

```python
by_category = full.groupby("category")["units_sold"].sum().sort_values(ascending=False)
print(by_category)
```

```text
Beauty & Personal Care    1394378
Grocery                   1346570
Electronics                977483
Sports & Fitness           791878
Clothing                   788145
Home Appliances            222811
```

Cheap, everyday goods sell the most units. Big-ticket items (air conditioners) sell the fewest.

![Monthly units by category](../images/charts/ch04-monthly-units-by-category.png)

> 🔎 Look at the wavy lines: demand rises and falls through the year. That is **seasonality**, and it is why a forecasting model needs holiday and calendar columns.

---

## 🧹 The data is not perfectly clean (on purpose)

Real data is messy. These CSVs contain realistic problems. **Do not fix them yet.** The Bronze layer keeps raw data exactly as it arrived, and the Silver layer cleans it.

| Problem | How to see it | Count |
|---|---|---|
| **Inconsistent text** in `channel_id` | `sales.channel_id.value_counts()` shows `Online` *and* `ONLINE`, `Physical Store` *and* `PHYSICAL STORE`, and so on | 849 rows use the UPPERCASE form (8 spellings instead of 4) |
| **Missing customer segment** | `sales.isna().sum()` | 2,321 |
| **Missing discount percentage** | same | 2,385 |
| **Missing inventory value** | same | 1,533 |
| **Hidden demand** from stockouts | `sales.stockout_flag.sum()` | 1,546 rows (about 1.8%) |

![Messy channel values](../images/charts/ch04-messy-channel-values.png)

### The stockout trap 🪤

When a shelf is empty, `units_sold` records what we *sold*, not what customers *wanted*. A model trained on raw sales would learn that demand is low on those days, which is wrong.

![Stockouts hide demand](../images/charts/ch04-stockout-hidden-demand.png)

The orange bars (`true_demand_estimate`) are far taller than the blue bars (`units_sold`) on stockout days. This synthetic file includes the "answer key" so we can *see* the effect. In real life you would not have it, and you would have to be careful. Chapter 7 (EDA) shows how the project looks at stockouts.

---

## 🔬 Where the data lives in Databricks

Later you will load these files into a **Unity Catalog Volume** (a folder for files), and then into **Delta tables** (Databricks' table format, like Excel with superpowers: fast, versioned and safe).

![Catalog explorer](../images/screenshots/ch04-catalog-explorer-tables.png)

> 📸 *After Chapter 5, add a screenshot of your Catalog Explorer here.*

---

## ✅ Checkpoint

1. How many rows are in the sales table? *(84,928)*
2. Which column is the **target** the model will predict? *(`units_sold`)*
3. Which three columns link sales to the other tables? *(`product_id`, `store_id`, `date`)*
4. In a star schema, can the `products` table link directly to `stores`? *(No. Only through sales.)*
5. After the left join, why must `len(full) == len(sales)` be `True`?

---

## 🔗 Learn more

- [pandas: 10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Star schema guidance (Microsoft Learn)](https://learn.microsoft.com/power-bi/guidance/star-schema)
- [Delta Lake introduction](https://docs.delta.io/latest/delta-intro.html)
- [What are Unity Catalog volumes?](https://learn.microsoft.com/azure/databricks/connect/unity-catalog/volumes)

⬅️ [Chapter 3](03-setup-and-costs.md) · ➡️ **Next:** [Chapter 5: Databricks setup and Bronze](05-databricks-setup-and-bronze.md)
