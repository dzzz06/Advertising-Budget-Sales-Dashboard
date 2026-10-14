from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Advertising Budget & Sales Dashboard",
    layout="wide",
)


DATA_PATH = Path(__file__).parent / "advertising.csv"
CHANNELS = ["TV", "Radio", "Newspaper"]


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and validate the small Kaggle snapshot used by the dashboard."""
    data = pd.read_csv(DATA_PATH)
    required = CHANNELS + ["Sales"]
    missing_columns = sorted(set(required) - set(data.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    if data[required].isna().any().any():
        raise ValueError("The dataset contains missing values in required columns.")
    return data[required].copy()


try:
    df = load_data()
except (FileNotFoundError, ValueError) as error:
    st.error(f"Could not load the advertising data: {error}")
    st.stop()


correlations = df[CHANNELS + ["Sales"]].corr(numeric_only=True)["Sales"].drop("Sales")
strongest_channel = correlations.abs().idxmax()
strongest_correlation = correlations[strongest_channel]
df["Total Spend"] = df[CHANNELS].sum(axis=1)


st.title("Advertising Budget & Sales Dashboard | Team 12")
st.caption(
    "For a marketing manager who needs a quick view of which advertising channels are most closely associated with sales."
)

st.info(
    "Decision focus: use the historical relationships in this snapshot to decide which channel deserves a closer budget review. "
    "Correlation is descriptive and does not prove that advertising caused the sales result."
)


metric_1, metric_2, metric_3 = st.columns(3)
metric_1.metric("Average sales", f"{df['Sales'].mean():.2f}")
metric_2.metric("Average total ad spend", f"{df['Total Spend'].mean():.2f}")
metric_3.metric(
    "Strongest historical channel",
    strongest_channel,
    f"r = {strongest_correlation:.2f}",
)

st.divider()

left, right = st.columns([1, 2])
with left:
    st.subheader("Channel comparison")
    correlation_data = (
        correlations.rename("Correlation")
        .rename_axis("Channel")
        .reset_index()
        .sort_values("Correlation", ascending=True)
    )
    correlation_chart = px.bar(
        correlation_data,
        x="Correlation",
        y="Channel",
        orientation="h",
        text=correlation_data["Correlation"].map(lambda value: f"{value:.2f}"),
        color="Correlation",
        color_continuous_scale="Blues",
        range_x=[0, 1],
    )
    correlation_chart.update_layout(
        height=360,
        coloraxis_showscale=False,
        xaxis_title="Correlation with sales",
        yaxis_title="",
        margin=dict(l=10, r=10, t=20, b=10),
    )
    correlation_chart.update_traces(textposition="outside")
    st.plotly_chart(correlation_chart, width="stretch")

with right:
    st.subheader("Selected channel and sales")
    selected_channel = st.selectbox(
        "Choose an advertising channel",
        CHANNELS,
        index=0,
        help="The marketing manager can inspect one channel at a time before reviewing its budget.",
    )

    x = df[selected_channel].to_numpy()
    y = df["Sales"].to_numpy()
    slope, intercept = np.polyfit(x, y, 1)
    line_x = np.linspace(x.min(), x.max(), 100)
    line_y = slope * line_x + intercept

    scatter_chart = go.Figure()
    scatter_chart.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            name="Market observations",
            marker=dict(color="#2563eb", size=8, opacity=0.72),
        )
    )
    scatter_chart.add_trace(
        go.Scatter(
            x=line_x,
            y=line_y,
            mode="lines",
            name="Linear trend",
            line=dict(color="#dc2626", width=3),
        )
    )
    scatter_chart.update_layout(
        height=360,
        xaxis_title=f"{selected_channel} advertising spend",
        yaxis_title="Sales",
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", y=1.12),
    )
    st.plotly_chart(scatter_chart, width="stretch")
    st.caption(
        f"Historical correlation for {selected_channel}: {correlations[selected_channel]:.2f}. "
        "The fitted line is a visual summary, not a causal forecast."
    )


st.divider()
st.caption(
    "Data period: 200 market observations from the Kaggle snapshot; the file has no date column. "
    "Intended production refresh: weekly after campaign data is updated."
)
