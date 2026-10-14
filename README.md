# Team 12: Advertising Budget & Sales Dashboard

This project is a small Streamlit dashboard for the BANA409 in-class group exercise. It uses the Kaggle [Advertising Dataset](https://www.kaggle.com/datasets/ashydv/advertising-dataset) and is designed for a marketing manager who needs a quick view of the relationship between advertising spend and sales. The project is presented as Team 12's work.

**Live app:** [Advertising Budget & Sales Dashboard](https://advertising-budget-sales-dashboard-krxst6gxxdm8rz82cazvgf.streamlit.app/)

## What the app shows

- Three headline metrics: average sales, average total advertising spend, and the channel with the strongest historical correlation with sales.
- A comparison of sales correlations for TV, Radio, and Newspaper advertising.
- A channel selector that updates a scatter plot and a simple fitted trend line.

The trend line summarizes the historical observations; it is not a causal estimate or a sales forecast.

## Step 1: Dataset and decision-maker

The dataset is a small CSV with 200 observations and four numeric columns:

- `TV`, `Radio`, and `Newspaper`: advertising spend for three channels.
- `Sales`: the sales outcome for the observation.

The CSV is a frozen Kaggle snapshot. It has no date column, so the dashboard treats each row as a market observation and does not claim to show a time trend. The file is small enough to keep in a public GitHub repository. The Kaggle page is the source for the original dataset description and units.

The dashboard is for one role: a marketing manager responsible for reviewing channel budgets. The manager would review it weekly after campaign data is updated.

## Step 2: Why this dashboard?

The decision is:

> If the marketing manager sees that one channel has a stronger or weaker historical relationship with sales, they will decide which channel needs a closer budget review for the next campaign cycle.

Without this dashboard, the manager would compare a spreadsheet of channel spend and sales manually. That takes time and makes it easy to miss the difference between channels. A dashboard is useful because the same comparison is repeated whenever the budget is reviewed. It puts the key comparison at the top and lets the manager inspect one selected channel without opening a separate analysis.

This dashboard is descriptive. A correlation or trend line does not prove that a channel caused sales, because the data does not include experiments, customer segments, prices, competitors, or campaign dates.

## Step 3: What matters on the page

The page order follows the decision:

1. **Top:** three headline metrics: average sales, average total advertising spend, and the channel with the strongest historical sales correlation.
2. **Middle:** a bar chart compares the three channel correlations. A selected-channel scatter plot shows the individual observations and a simple trend line.
3. **Bottom:** a short data-period and refresh note. A raw data table is intentionally omitted because the manager needs a budget comparison rather than row-by-row inspection.

The only filter is the advertising channel selector. It changes the scatter plot and gives the manager a focused view of TV, Radio, or Newspaper.

Two things are intentionally not shown:

- A time-series chart is omitted because the CSV has no date field.
- Extra distribution charts and a full raw-data table are omitted because they would add detail without changing the initial budget-review decision.

Potentially misleading aspects are called out in the app. Correlation is not causation, the dataset is a static snapshot, and the absence of dates means that the dashboard cannot measure recent growth or seasonality. The input columns are kept in the dataset's numeric units rather than converted to new business claims.

## Step 4: Refresh and review decision

In a production version, the data would refresh weekly after the campaign reporting data is updated. The marketing manager would review the dashboard once a week during the budget meeting. The tracked action metric would be sales per unit of total advertising spend. If that metric stayed at least 10% below its historical baseline for several weeks, the manager would investigate channel allocation and campaign performance.

The current Kaggle file cannot demonstrate a real weekly change because it has no dates. The weekly refresh statement is the intended production workflow, while the app itself demonstrates the page structure and historical comparison.

## Run locally

```text
uv run streamlit run app.py
```

For Streamlit Cloud, use `app.py` as the main file and set the Python version to 3.14 under Advanced settings, as required by the exercise.
