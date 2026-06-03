import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="E-Commerce Sales Intelligence",
    page_icon="📊",
    layout="wide"
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

filtered_master = master[
    master["order_year"] == selected_year
]

# Download button
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

    monthly["order_month"] = pd.to_datetime(
        monthly["order_month"]
    )

    fig = px.line(
        monthly,
        x="order_month",
        y="total_revenue",
        markers=True,
        title="Monthly Revenue Growth",
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

    rfm_counts = (
        rfm["rfm_segment"]
        .value_counts()
        .reset_index()
    )

    rfm_counts.columns = [
        "Segment",
        "Customers"
    ]

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

    # Revenue by segment

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

# ==========================================
# TAB 3 — SELLER ANALYTICS
# ==========================================

with tab3:

    st.subheader("🏪 Top Seller Performance")

    fig_sellers = px.bar(

        sellers,

        x="seller_id",

        y="total_revenue",

        color="total_revenue",

        title="Top Sellers by Revenue"
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

    state_chart = state.sort_values(
        "total_orders",
        ascending=False
    )

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

    st.subheader("📅 Cohort Retention Analysis")

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

    fig_cohort.update_xaxes(
        tickvals=list(range(len(cohort))),
        ticktext=cohort["cohort_month"]
    )

    fig_cohort.update_layout(
        title="Customer Retention Heatmap"
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

    st.success("""
    ✅ Revenue shows strong month-over-month growth trends.
    """)

    st.info("""
    📦 High-value customer segments contribute majority revenue.
    """)

    st.warning("""
    🚚 Delivery delays negatively impact customer review scores.
    """)

    st.error("""
    🏪 Top sellers dominate marketplace revenue contribution.
    """)

    st.markdown("---")

    st.subheader("📌 Business Recommendations")

    st.markdown("""
    - Improve logistics infrastructure in high-delay states.
    - Launch loyalty programs for high-value customers.
    - Support underperforming sellers with onboarding programs.
    - Reduce delivery delays to improve customer satisfaction.
    - Focus marketing campaigns on high-retention customer segments.
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
