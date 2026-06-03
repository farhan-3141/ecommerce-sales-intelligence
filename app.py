import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="E-Commerce Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main background */
.main {
    background-color: #F8FAFC;
}

/* KPI Cards */
[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #E5E7EB;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    width: 260px !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white;
}

/* Titles */
h1, h2, h3 {
    color: #111827;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 18px;
    font-weight: 600;
    padding: 10px 20px;
}

/* Chart spacing */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================


def load_data():

    master = pd.read_csv("olist_master_powerbi.csv")

    return master

master = load_data()

# ==========================================
# DATA PREPARATION
# ==========================================

master["order_purchase_timestamp"] = pd.to_datetime(
    master["order_purchase_timestamp"]
)

master["order_month"] = pd.to_datetime(
    master["order_month"]
)

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("📌 Dashboard Filters")

years = sorted(master["order_year"].dropna().unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    years,
    index=len(years)-1
)

# ==========================================
# FILTER DATA
# ==========================================

filtered_master = master[
    master["order_year"] == selected_year
]

# ==========================================
# DOWNLOAD BUTTON
# ==========================================

csv = filtered_master.to_csv(index=False)

st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

# ==========================================
# DASHBOARD TITLE
# ==========================================

st.title("📊 E-Commerce Sales Intelligence Dashboard")

st.markdown("""
Interactive Business Intelligence Dashboard built using
Streamlit + SQL + Python Analytics
""")

st.markdown("""
[🔗 GitHub Repository](https://github.com/farhan-3141/ecommerce-sales-intelligence)
|
[🚀 Live Dashboard](https://ecommerce-sales-intelligence-farhan.streamlit.app/)
""")

# ==========================================
# KPI CALCULATIONS
# ==========================================

total_revenue = filtered_master["price"].sum()

total_orders = filtered_master["order_id"].nunique()

avg_order = filtered_master["price"].mean()

avg_review = filtered_master["review_score"].mean()

# ==========================================
# KPI CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"R$ {total_revenue/1000:.1f}K"
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

st.markdown("---")

# ==========================================
# CREATE DYNAMIC ANALYTICS
# ==========================================

# Ensure datetime conversion
filtered_master["order_purchase_timestamp"] = pd.to_datetime(
    filtered_master["order_purchase_timestamp"]
)

# ------------------------------------------
# MONTHLY REVENUE
# ------------------------------------------

monthly = (
    filtered_master
    .groupby(
        filtered_master["order_purchase_timestamp"].dt.to_period("M")
    )
    .agg(
        total_revenue=("price", "sum")
    )
    .reset_index()
)

monthly["order_month"] = monthly[
    "order_purchase_timestamp"
].astype(str)

# ------------------------------------------
# RFM ANALYSIS
# ------------------------------------------

customer_rfm = (
    filtered_master
    .groupby("customer_city")
    .agg(
        frequency=("order_id", "nunique"),
        monetary=("price", "sum")
    )
    .reset_index()
)

customer_rfm["Segment"] = "Low Value"

customer_rfm.loc[
    customer_rfm["monetary"] > 100,
    "Segment"
] = "Medium Value"

customer_rfm.loc[
    customer_rfm["monetary"] > 500,
    "Segment"
] = "High Value"

customer_rfm.loc[
    customer_rfm["monetary"] > 1000,
    "Segment"
] = "Champions"
rfm_counts = (
    customer_rfm["Segment"]
    .value_counts()
    .reset_index()
)

rfm_counts.columns = [
    "Segment",
    "Customers"
]

segment_revenue = (
    customer_rfm
    .groupby("Segment")["monetary"]
    .sum()
    .reset_index()
)

# ------------------------------------------
# SELLER ANALYSIS
# ------------------------------------------

seller_analysis = (
    filtered_master
    .groupby("seller_id")
    .agg(
        total_revenue=("price", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
    .sort_values(
        "total_revenue",
        ascending=False
    )
    .head(10)
)

# ------------------------------------------
# STATE ANALYSIS
# ------------------------------------------

state_analysis = (
    filtered_master
    .groupby("customer_state")
    .agg(
        total_orders=("order_id", "nunique"),
        avg_delivery_days=("delivery_days", "mean"),
        avg_review=("review_score", "mean")
    )
    .reset_index()
)

# ------------------------------------------
# RETENTION ANALYSIS
# ------------------------------------------

cohort_analysis = (
    filtered_master
    .groupby(
        filtered_master["order_purchase_timestamp"].dt.to_period("M")
    )
    .agg(
        total_customers=("customer_city", "nunique")
    )
    .reset_index()
)

cohort_analysis["order_month"] = cohort_analysis[
    "order_purchase_timestamp"
].astype(str)
# ==========================================
# DASHBOARD TABS
# ==========================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "👥 Customer Analytics",
    "🏪 Seller Analytics",
    "🌎 Geographic Insights",
    "📅 Retention Analytics",
    "🧠 Executive Insights"
])

# ==========================================
# TAB 1 — OVERVIEW
# ==========================================

with tab1:

    st.subheader("📈 Monthly Revenue Trend")

    fig = px.line(
        monthly,
        x="order_month",
        y="total_revenue",
        markers=True,
        title=f"Monthly Revenue Growth - {selected_year}",
        height=500
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (R$)",
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# TAB 2 — CUSTOMER ANALYTICS
# ==========================================

with tab2:

    st.subheader("👥 RFM Customer Segmentation")

    fig_rfm = px.pie(
        rfm_counts,
        names="Segment",
        values="Customers",
        title=f"Customer Segmentation - {selected_year}"
    )

    st.plotly_chart(
        fig_rfm,
        use_container_width=True
    )

    fig_bar = px.bar(
        segment_revenue,
        x="Segment",
        y="monetary",
        title=f"Revenue by Segment - {selected_year}",
        color="Segment"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

# ==========================================
# TAB 3 — SELLER ANALYTICS
# ==========================================

with tab3:

    st.subheader("🏪 Top Seller Performance")

    fig_sellers = px.bar(

        seller_analysis,

        x="seller_id",

        y="total_revenue",

        color="total_revenue",

        title=f"Top Sellers - {selected_year}"
    )

    fig_sellers.update_layout(

        xaxis_title="Seller ID",

        yaxis_title="Revenue (R$)",

        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_sellers,
        use_container_width=True
    )

# ==========================================
# TAB 4 — GEOGRAPHIC INSIGHTS
# ==========================================

with tab4:

    st.subheader("🌎 State-wise Order Analysis")

    fig_state = px.bar(

        state_analysis,

        x="customer_state",

        y="total_orders",

        color="avg_review",

        title=f"Orders by State - {selected_year}",

        hover_data=[
            "avg_delivery_days",
            "avg_review"
        ]
    )

    fig_state.update_layout(

        xaxis_title="State",

        yaxis_title="Total Orders",

        template="plotly_white"
    )

    st.plotly_chart(
        fig_state,
        use_container_width=True
    )

# ==========================================
# TAB 5 — RETENTION ANALYTICS
# ==========================================

with tab5:

    st.subheader("📅 Customer Retention Trend")

    fig_cohort = px.area(

        cohort_analysis,

        x="order_month",

        y="total_customers",

        title=f"Customer Activity Trend - {selected_year}"
    )

    fig_cohort.update_layout(
        xaxis_title="Month",
        yaxis_title="Active Customers"
    )

    st.plotly_chart(
        fig_cohort,
        use_container_width=True
    )

# ==========================================
# TAB 6 — EXECUTIVE INSIGHTS
# ==========================================

with tab6:

    st.subheader("🧠 Executive Business Insights")

    top_state = (
        state_analysis
        .sort_values(
            "total_orders",
            ascending=False
        )
        .iloc[0]["customer_state"]
    )

    top_segment = (
        segment_revenue
        .sort_values(
            "monetary",
            ascending=False
        )
        .iloc[0]["Segment"]
    )

    st.success(f"""
    ✅ Highest revenue observed in {selected_year}.
    """)

    st.info(f"""
    📦 Top customer segment: {top_segment}
    """)

    st.warning(f"""
    🚚 State with highest orders: {top_state}
    """)

    st.error("""
    🏪 Top sellers contribute major marketplace revenue.
    """)

    st.markdown("---")

    st.subheader("📌 Business Recommendations")

    st.markdown(f"""
    - Focus marketing campaigns on high-value customers in {selected_year}.
    - Improve logistics efficiency in high-volume states.
    - Retain top-performing sellers through incentives.
    - Optimize customer experience to improve review ratings.
    - Expand operations in high-performing regions.
    """)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <center>
    Built with ❤️ by <b>Farhan Ansari</b> | IIT (ISM) Dhanbad
    </center>
    """,
    unsafe_allow_html=True
)
