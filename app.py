import streamlit as st
import pandas as pd

# --------------------------------
# Page Config
# --------------------------------

st.set_page_config(
    page_title="E-Commerce Sales Intelligence",
    page_icon="📊",
    layout="wide"
)
# --------------------------------
# Custom Dashboard Styling
# --------------------------------

st.markdown("""
<style>

/* Main background */
.main {
    background-color: #F8FAFC;
}

/* KPI metric cards */
[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #E5E7EB;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white;
}

/* Titles */
h1, h2, h3 {
    color: #111827;
}

/* Chart spacing */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)
# --------------------------------
# Load Data
# --------------------------------

@st.cache_data
def load_data():

    master = pd.read_csv("olist_master_powerbi.csv")

    rfm = pd.read_csv("rfm_segments.csv")

    state = pd.read_csv("state_summary.csv")

    sellers = pd.read_csv("top_sellers.csv")

    cohort = pd.read_csv("cohort_retention.csv")

    monthly = pd.read_csv("monthly_revenue.csv")

    return master, rfm, state, sellers, cohort, monthly

master, rfm, state, sellers, cohort, monthly = load_data()
# --------------------------------
# Sidebar Filters
# --------------------------------

st.sidebar.header("📌 Dashboard Filters")

# Available years
years = sorted(master["order_year"].dropna().unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

# Filter dataset
filtered_master = master[
    master["order_year"] == selected_year
]

# --------------------------------
# Dashboard Title
# --------------------------------

st.title("📊 E-Commerce Sales Intelligence Dashboard")

st.markdown("""
Interactive Business Intelligence Dashboard
built using Streamlit + SQL + Python Analytics
""")

# --------------------------------
# KPI Calculations
# --------------------------------

total_revenue = filtered_master["price"].sum()

total_orders = filtered_master["order_id"].nunique()

avg_order = filtered_master["price"].mean()

avg_review = filtered_master["review_score"].mean()

# KPI Cards
# --------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"R$ {total_revenue:,.0f}"
)

col2.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Average Order Value",
    f"R$ {avg_order:.2f}"
)

col4.metric(
    "Average Review",
    f"{avg_review:.2f} ⭐"
)


# --------------------------------
# Sample Data
# --------------------------------

st.subheader("📦 Sample Dataset")

st.dataframe(filtered_master.head(10))

# --------------------------------
# Revenue Trend Chart
# --------------------------------

import plotly.express as px

st.subheader("📈 Monthly Revenue Trend")

# Convert month column
monthly["order_month"] = pd.to_datetime(
    monthly["order_month"]
)

# Create line chart
fig = px.line(
    monthly,
    x="order_month",
    y="total_revenue",
    markers=True,
    title="Monthly Revenue Growth"
)

# Improve layout
fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue (R$)",
    template="plotly_white"
)

# Display chart
st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------
# RFM Segment Analysis
# --------------------------------

st.subheader("👥 RFM Customer Segmentation")

# Count segments
rfm_counts = (
    rfm["rfm_segment"]
    .value_counts()
    .reset_index()
)

rfm_counts.columns = [
    "Segment",
    "Customers"
]

# Pie Chart
fig_rfm = px.pie(
    rfm_counts,
    names="Segment",
    values="Customers",
    title="Customer Distribution by RFM Segment"
)

st.plotly_chart(
    fig_rfm,
    use_container_width=True
)

# --------------------------------
# Revenue by Segment
# --------------------------------

segment_revenue = (
    rfm.groupby("rfm_segment")["monetary"]
    .sum()
    .reset_index()
)

fig_bar = px.bar(
    segment_revenue,
    x="rfm_segment",
    y="monetary",
    title="Revenue Contribution by Segment",
    color="rfm_segment"
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)
# --------------------------------
# Seller Performance Analysis
# --------------------------------

st.subheader("🏪 Top Seller Performance")

# Top sellers chart
fig_sellers = px.bar(

    sellers,

    x="seller_id",

    y="total_revenue",

    color="total_revenue",

    title="Top Sellers by Revenue"
)

# Improve layout
fig_sellers.update_layout(

    xaxis_title="Seller ID",

    yaxis_title="Revenue (R$)",

    xaxis_tickangle=-45
)

# Display chart
st.plotly_chart(
    fig_sellers,
    use_container_width=True
)
# --------------------------------
# Geographic State Analysis
# --------------------------------

st.subheader("🌎 State-wise Order Analysis")

# Sort states
state_chart = state.sort_values(
    "total_orders",
    ascending=False
)

# Create chart
fig_state = px.bar(

    state_chart,

    x="customer_state",

    y="total_orders",

    color="on_time_pct",

    title="Orders by Brazilian State",

    hover_data=[
        "avg_delivery_days",
        "on_time_pct"
    ]
)

# Layout improvements
fig_state.update_layout(

    xaxis_title="State",

    yaxis_title="Total Orders",

    template="plotly_white"
)

# Display chart
st.plotly_chart(
    fig_state,
    use_container_width=True
)
# --------------------------------
# Cohort Retention Analysis
# --------------------------------

st.subheader("📅 Cohort Retention Analysis")

# Create heatmap-style chart
fig_cohort = px.imshow(

    cohort[["retention_pct"]].T,

    text_auto=True,

    aspect="auto",

    color_continuous_scale="Blues",

    labels=dict(
        x="Cohort Month",
        y="Retention",
        color="Retention %"
    )
)

# Update x-axis labels
fig_cohort.update_xaxes(
    tickvals=list(range(len(cohort))),
    ticktext=cohort["cohort_month"]
)

# Layout
fig_cohort.update_layout(
    title="Customer Retention Heatmap"
)

# Display chart
st.plotly_chart(
    fig_cohort,
    use_container_width=True
)