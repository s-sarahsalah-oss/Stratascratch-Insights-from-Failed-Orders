# Insights from Failed Orders

An exploratory data analysis of ride/delivery orders that failed to complete, looking at *why* orders fail (client cancellations vs. system rejections, before vs. after driver assignment), *when* they fail (by hour of day), and *where* they fail (geospatially, using H3 hexagons).

## Data

Two source CSV files are merged on `order_gk` (order key):

- **`data_orders.csv`** — one row per order, with:
  - `order_datetime` — time the order was placed
  - `origin_latitude` / `origin_longitude` — pickup location
  - `m_order_eta` — estimated time of arrival (minutes)
  - `order_status_key` — `4` = Client Cancelled, `9` = System Rejected
  - `is_driver_assigned_key` — whether a driver had been assigned (`0` = No, `1` = Yes)
  - `cancellations_time_in_seconds` — time elapsed before cancellation
- **`data_offers.csv`** — one row per `offer_id`, linking offers made to an `order_gk`

After an inner merge, the combined dataset (`df`) has one row per order/offer pair (~31k rows), with status and assignment codes mapped to readable labels (`"Client Cancelled"` / `"System Rejected"`, `"Yes"` / `"No"`).

## Requirements

```
pandas
numpy
matplotlib
folium
h3
```

## Analysis & Key Findings

### 1. Reasons for failure
Orders are split into four buckets: cancelled before/after driver assignment, and rejected by the system before/after assignment. A bar chart shows the count in each bucket — **cancellations before a driver was assigned** are the largest failure category, followed by cancellations after assignment; system rejections occur almost entirely before assignment.

### 2. Failures by hour of day
A line chart of total failed orders grouped by hour reveals clear peaks — failures cluster around specific hours (e.g., evening/rush-hour periods), suggesting failure rates track overall demand and driver-availability strain rather than being random.

### 3. Failures by hour, split by status and assignment
Breaking the hourly trend down by `is_driver_assigned_key` × `order_status_key` shows that "no driver assigned" cancellations and system rejections dominate at nearly every hour, while post-assignment cancellations are comparatively flat throughout the day.

### 4. Average cancellation time by hour
The average time-to-cancellation is plotted separately for orders with vs. without an assigned driver, by hour. Cancellations **after a driver is assigned consistently take longer** (customers wait longer before giving up) than cancellations with no driver assigned, across almost all hours — with some volatility that outliers may be inflating (the notebook flags outlier removal as a possible refinement).

### 5. Average ETA by hour
Average `m_order_eta` by hour shows ETA rising during busier periods (e.g., morning peak) and dropping in low-traffic hours — consistent with higher demand or fewer available drivers pushing estimated wait times up.

### 6. Bonus: Geospatial hotspots (H3 hexagons)
Using `h3.latlng_to_cell` (resolution 8), each order's pickup point is mapped to a hexagonal cell. Cells are ranked by order volume and cumulative share of total orders:

- **137 hexagons** account for the first ~80% of all orders/failures.
- Just **2 hexagons** ("hotspots") account for the remaining ~20%, with one alone holding ~4,488 orders.

These hotspot hexes are visualized on an interactive `folium` map (`map.html`), colored red (top bottleneck hexes, >80th percentile) vs. blue (all others), to highlight where operational focus (driver supply, dispatch tuning) would have the most impact.

## Files

| File | Description |
|---|---|
| `Insights_from_Failed_Orders.ipynb` | Full analysis notebook |
| `data_orders.csv` | Order-level source data (not included here — supply your own) |
| `data_offers.csv` | Offer-level source data (not included here — supply your own) |
| `map.html` | Generated interactive map of failure hotspots (output of the notebook) |

## How to Run

1. Place `data_orders.csv` and `data_offers.csv` in the same directory as the notebook.
2. Install dependencies: `pip install pandas numpy matplotlib folium h3`
3. Run all cells in `Insights_from_Failed_Orders.ipynb` top to bottom.
4. Open the generated `map.html` in a browser to explore the hotspot map interactively.