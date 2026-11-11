import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta

st.set_page_config(
    page_title="MedStock AI | Medicine Intelligence",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
:root { --primary: #167D9A; }
.block-container { padding-top: 1.4rem; padding-bottom: 2rem; }
[data-testid="stSidebar"] { background: #F4F8FB; }
.hero {
    padding: 1.35rem 1.6rem; border-radius: 18px;
    background: linear-gradient(115deg, #0C536B 0%, #167D9A 58%, #35A7A0 100%);
    color: white; margin-bottom: 1.2rem;
}
.hero h1 { color: white; font-size: 2.1rem; margin: 0 0 .25rem 0; }
.hero p { color: #EAF8FC; margin: 0; font-size: 1rem; }
.demo-note {
    padding: .7rem 1rem; border-radius: 10px; background: #FFF7E6;
    border: 1px solid #F2D28B; color: #75520A; font-size: .9rem;
}
.metric-label { color: #64748B; font-size: .86rem; }
.section-sub { color: #64748B; margin-top: -0.5rem; }
div[data-testid="stMetric"] {
    background: #FFFFFF; border: 1px solid #E5EDF2;
    padding: 1rem; border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Clearly labeled demo data ----------
@st.cache_data
def make_demo_data():
    meds = [
        {"Medicine": "Paracetamol 500 mg", "Category": "Analgesic", "Stock": 420, "Daily Usage": 52, "Lead Time (days)": 3, "Safety Stock": 100, "Unit Cost (₹)": 1.8, "Expiry": date.today() + timedelta(days=210), "Supplier": "Apollo MedSupply"},
        {"Medicine": "Amoxicillin 250 mg", "Category": "Antibiotic", "Stock": 85, "Daily Usage": 24, "Lead Time (days)": 5, "Safety Stock": 80, "Unit Cost (₹)": 4.5, "Expiry": date.today() + timedelta(days=155), "Supplier": "CareFirst Distributors"},
        {"Medicine": "Cetirizine 10 mg", "Category": "Antihistamine", "Stock": 260, "Daily Usage": 18, "Lead Time (days)": 4, "Safety Stock": 60, "Unit Cost (₹)": 1.2, "Expiry": date.today() + timedelta(days=300), "Supplier": "Apollo MedSupply"},
        {"Medicine": "ORS Sachet", "Category": "Rehydration", "Stock": 48, "Daily Usage": 20, "Lead Time (days)": 2, "Safety Stock": 50, "Unit Cost (₹)": 7.0, "Expiry": date.today() + timedelta(days=95), "Supplier": "HealthBridge Wholesale"},
        {"Medicine": "Metformin 500 mg", "Category": "Antidiabetic", "Stock": 330, "Daily Usage": 31, "Lead Time (days)": 4, "Safety Stock": 90, "Unit Cost (₹)": 2.3, "Expiry": date.today() + timedelta(days=240), "Supplier": "CareFirst Distributors"},
        {"Medicine": "Salbutamol Inhaler", "Category": "Respiratory", "Stock": 32, "Daily Usage": 9, "Lead Time (days)": 6, "Safety Stock": 35, "Unit Cost (₹)": 95.0, "Expiry": date.today() + timedelta(days=180), "Supplier": "RespiraCare Ltd"},
        {"Medicine": "Omeprazole 20 mg", "Category": "Gastrointestinal", "Stock": 190, "Daily Usage": 16, "Lead Time (days)": 4, "Safety Stock": 55, "Unit Cost (₹)": 3.1, "Expiry": date.today() + timedelta(days=270), "Supplier": "Apollo MedSupply"},
        {"Medicine": "Iron + Folic Acid", "Category": "Supplement", "Stock": 110, "Daily Usage": 15, "Lead Time (days)": 5, "Safety Stock": 70, "Unit Cost (₹)": 2.0, "Expiry": date.today() + timedelta(days=120), "Supplier": "HealthBridge Wholesale"},
        {"Medicine": "Azithromycin 500 mg", "Category": "Antibiotic", "Stock": 74, "Daily Usage": 12, "Lead Time (days)": 6, "Safety Stock": 55, "Unit Cost (₹)": 8.5, "Expiry": date.today() + timedelta(days=190), "Supplier": "CareFirst Distributors"},
        {"Medicine": "Vitamin C 500 mg", "Category": "Supplement", "Stock": 520, "Daily Usage": 22, "Lead Time (days)": 3, "Safety Stock": 70, "Unit Cost (₹)": 1.5, "Expiry": date.today() + timedelta(days=330), "Supplier": "HealthBridge Wholesale"},
        {"Medicine": "Ibuprofen 200 mg", "Category": "Analgesic", "Stock": 95, "Daily Usage": 21, "Lead Time (days)": 3, "Safety Stock": 65, "Unit Cost (₹)": 2.1, "Expiry": date.today() + timedelta(days=165), "Supplier": "Apollo MedSupply"},
        {"Medicine": "Cough Syrup 100 ml", "Category": "Respiratory", "Stock": 58, "Daily Usage": 14, "Lead Time (days)": 4, "Safety Stock": 45, "Unit Cost (₹)": 38.0, "Expiry": date.today() + timedelta(days=80), "Supplier": "RespiraCare Ltd"},
    ]
    df = pd.DataFrame(meds)
    # Generate illustrative 90-day history with repeatable variation and mild trend.
    rng = np.random.default_rng(24)
    records = []
    for idx, row in df.iterrows():
        base_usage = float(row["Daily Usage"])
        start = date.today() - timedelta(days=89)
        for d in range(90):
            day = start + timedelta(days=d)
            weekday_factor = 1.12 if day.weekday() in (0, 1) else (0.92 if day.weekday() == 6 else 1.0)
            seasonal_factor = 1 + 0.10 * np.sin(2 * np.pi * d / 30)
            trend_factor = 1 + (0.0008 * d * (1 if idx % 3 == 0 else -0.25))
            usage = max(0, int(round(base_usage * weekday_factor * seasonal_factor * trend_factor + rng.normal(0, max(1, base_usage * .09)))))
            records.append({"Date": day, "Medicine": row["Medicine"], "Units Used": usage})
    history = pd.DataFrame(records)
    return df, history

if "inventory" not in st.session_state:
    inventory, history = make_demo_data()
    st.session_state.inventory = inventory.copy()
    st.session_state.history = history.copy()

inventory = st.session_state.inventory.copy()
history = st.session_state.history.copy()

def status_for(row):
    days_cover = row["Stock"] / max(row["Daily Usage"], 1)
    if row["Stock"] <= row["Daily Usage"] * row["Lead Time (days)"]:
        return "Critical"
    if row["Stock"] <= row["Safety Stock"] or days_cover <= row["Lead Time (days)"] + 3:
        return "Low"
    return "Healthy"

inventory["Days of Cover"] = (inventory["Stock"] / inventory["Daily Usage"]).round(1)
inventory["Status"] = inventory.apply(status_for, axis=1)
inventory["Lead-time Demand"] = inventory["Daily Usage"] * inventory["Lead Time (days)"]
inventory["Suggested Reorder"] = (
    inventory["Daily Usage"] * (inventory["Lead Time (days)"] + 7)
    + inventory["Safety Stock"] - inventory["Stock"]
).clip(lower=0).round().astype(int)
inventory["Estimated Stock Value (₹)"] = inventory["Stock"] * inventory["Unit Cost (₹)"]

# ---------- Sidebar ----------
st.sidebar.markdown("## 💊 MedStock AI")
st.sidebar.caption("Medicine demand & inventory intelligence")
page = st.sidebar.radio(
    "Navigate",
    ["Overview Dashboard", "Medicine Inventory", "Demand Forecast", "Stock Risk & Reorder"],
)
st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")
category_options = ["All categories"] + sorted(inventory["Category"].unique().tolist())
selected_category = st.sidebar.selectbox("Medicine category", category_options)
status_options = ["All statuses", "Critical", "Low", "Healthy"]
selected_status = st.sidebar.selectbox("Stock status", status_options)
st.sidebar.markdown("---")
st.sidebar.caption("Prototype • Demo dataset • Not for clinical decisions")

if selected_category != "All categories":
    inventory = inventory[inventory["Category"] == selected_category]
if selected_status != "All statuses":
    inventory = inventory[inventory["Status"] == selected_status]

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <h1>💊 MedStock AI</h1>
  <p>Intelligent medicine demand forecasting & inventory optimization</p>
</div>
<div class="demo-note"><b>DEMO MODE:</b> All medicine inventory and usage values in this prototype are illustrative sample data, not live hospital/pharmacy records. Forecasts are estimates for demonstration only.</div>
""", unsafe_allow_html=True)
st.write("")

# ---------- Pages ----------
if page == "Overview Dashboard":
    st.subheader("Overview dashboard")
    st.markdown('<p class="section-sub">A quick view of inventory health and demand signals.</p>', unsafe_allow_html=True)

    total_items = len(inventory)
    critical_count = int((inventory["Status"] == "Critical").sum())
    low_count = int((inventory["Status"] == "Low").sum())
    total_units = int(inventory["Stock"].sum())
    stock_value = float(inventory["Estimated Stock Value (₹)"].sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Medicines tracked", f"{total_items}")
    c2.metric("Critical stock", f"{critical_count}", delta="Immediate review" if critical_count else "No critical items", delta_color="inverse" if critical_count else "normal")
    c3.metric("Low stock", f"{low_count}")
    c4.metric("Inventory value", f"₹{stock_value:,.0f}")

    st.write("")
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("#### Stock status")
        status_counts = inventory["Status"].value_counts().reindex(["Healthy", "Low", "Critical"], fill_value=0).reset_index()
        status_counts.columns = ["Status", "Medicines"]
        fig = px.pie(status_counts, names="Status", values="Medicines", hole=.62,
                     color="Status", color_discrete_map={"Healthy": "#24A27A", "Low": "#E7A23B", "Critical": "#D9534F"})
        fig.update_layout(margin=dict(t=10,b=10,l=10,r=10), legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown("#### Stock coverage by medicine")
        chart_df = inventory.sort_values("Days of Cover", ascending=True)
        fig = px.bar(chart_df, x="Days of Cover", y="Medicine", orientation="h", color="Status",
                     color_discrete_map={"Healthy": "#24A27A", "Low": "#E7A23B", "Critical": "#D9534F"},
                     labels={"Days of Cover": "Days of stock remaining", "Medicine": ""})
        fig.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=370, legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Items needing attention")
    attention = inventory[inventory["Status"].isin(["Critical", "Low"])].sort_values("Days of Cover")
    if attention.empty:
        st.success("No low or critical stock items in the current filter.")
    else:
        st.dataframe(attention[["Medicine", "Category", "Stock", "Daily Usage", "Days of Cover", "Lead Time (days)", "Status", "Suggested Reorder"]], hide_index=True, use_container_width=True)
    st.caption("Stock status is a simple planning indicator based on demo daily usage, lead time and safety stock.")

elif page == "Medicine Inventory":
    st.subheader("Medicine inventory")
    st.markdown('<p class="section-sub">Review stock levels, suppliers, expiry dates and planning indicators.</p>', unsafe_allow_html=True)
    search = st.text_input("Search medicine", placeholder="e.g., Paracetamol")
    view = inventory.copy()
    if search:
        view = view[view["Medicine"].str.contains(search, case=False, na=False)]
    display_cols = ["Medicine", "Category", "Stock", "Daily Usage", "Days of Cover", "Lead Time (days)", "Safety Stock", "Expiry", "Supplier", "Status"]
    st.dataframe(view[display_cols], hide_index=True, use_container_width=True,
                 column_config={
                     "Expiry": st.column_config.DateColumn("Expiry date", format="DD MMM YYYY"),
                     "Stock": st.column_config.NumberColumn("Stock (units)", format="%d"),
                     "Daily Usage": st.column_config.NumberColumn("Avg. daily usage", format="%d"),
                     "Days of Cover": st.column_config.NumberColumn("Days of cover", format="%.1f"),
                 })
    with st.expander("➕ Add a demo inventory item"):
        with st.form("add_medicine_form"):
            name = st.text_input("Medicine name")
            category = st.selectbox("Category", ["Analgesic", "Antibiotic", "Antihistamine", "Rehydration", "Antidiabetic", "Respiratory", "Supplement", "Other"])
            stock = st.number_input("Current stock (units)", min_value=0, value=100, step=10)
            daily = st.number_input("Average daily usage (units)", min_value=1, value=10, step=1)
            lead = st.number_input("Supplier lead time (days)", min_value=1, value=3, step=1)
            safety = st.number_input("Safety stock (units)", min_value=0, value=30, step=5)
            cost = st.number_input("Unit cost (₹)", min_value=0.0, value=5.0, step=0.5)
            expiry = st.date_input("Expiry date", value=date.today() + timedelta(days=180))
            supplier = st.text_input("Supplier", value="Demo Supplier")
            submitted = st.form_submit_button("Add medicine")
        if submitted:
            if not name.strip():
                st.error("Enter a medicine name.")
            elif name.strip().lower() in st.session_state.inventory["Medicine"].str.lower().tolist():
                st.error("That medicine name already exists in the demo inventory.")
            else:
                new_row = {
                    "Medicine": name.strip(), "Category": category, "Stock": int(stock),
                    "Daily Usage": int(daily), "Lead Time (days)": int(lead), "Safety Stock": int(safety),
                    "Unit Cost (₹)": float(cost), "Expiry": expiry, "Supplier": supplier.strip() or "Demo Supplier",
                }
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Added {name.strip()} to this session's inventory.")
                st.rerun()
    st.download_button("⬇️ Download current inventory CSV", data=st.session_state.inventory.to_csv(index=False).encode("utf-8"),
                       file_name="medstock_demo_inventory.csv", mime="text/csv")

elif page == "Demand Forecast":
    st.subheader("Medicine demand forecasting")
    st.markdown('<p class="section-sub">A simple baseline forecast based on recent historical usage. Use real, validated data before operational decisions.</p>', unsafe_allow_html=True)
    all_meds = st.session_state.inventory["Medicine"].tolist()
    chosen = st.selectbox("Choose medicine", all_meds)
    hist = history[history["Medicine"] == chosen].sort_values("Date").copy()
    recent_days = st.slider("Recent history used for baseline", min_value=7, max_value=60, value=30, step=1)
    horizon = st.slider("Forecast horizon (days)", min_value=7, max_value=30, value=14, step=7)

    recent = hist.tail(recent_days)
    # Baseline: weighted recent average, not a trained ML model.
    last7 = recent.tail(min(7, len(recent)))["Units Used"].mean()
    last30 = recent["Units Used"].mean()
    forecast_daily = max(0, 0.65 * last7 + 0.35 * last30)
    trend = np.polyfit(np.arange(len(recent)), recent["Units Used"].values, 1)[0] if len(recent) > 1 else 0
    forecast_dates = [date.today() + timedelta(days=i) for i in range(1, horizon + 1)]
    # Slight trend adjustment, capped to avoid unstable extrapolation.
    forecast_values = [max(0, forecast_daily + np.clip(trend, -forecast_daily * .03, forecast_daily * .03) * i) for i in range(1, horizon + 1)]
    forecast = pd.DataFrame({"Date": forecast_dates, "Estimated units used": np.round(forecast_values).astype(int)})
    med_row = st.session_state.inventory[st.session_state.inventory["Medicine"] == chosen].iloc[0]
    demand_total = int(forecast["Estimated units used"].sum())
    avg_forecast = float(forecast["Estimated units used"].mean())
    m1, m2, m3 = st.columns(3)
    m1.metric("Estimated demand", f"{demand_total:,} units", f"next {horizon} days")
    m2.metric("Estimated daily demand", f"{avg_forecast:.1f} units/day")
    m3.metric("Current stock", f"{int(med_row['Stock']):,} units")

    hist_plot = hist.tail(recent_days).rename(columns={"Units Used": "Units"})
    hist_plot["Type"] = "Historical usage"
    future_plot = forecast.rename(columns={"Estimated units used": "Units"})
    future_plot["Type"] = "Baseline forecast"
    plot_df = pd.concat([hist_plot[["Date", "Units", "Type"]], future_plot[["Date", "Units", "Type"]]], ignore_index=True)
    fig = px.line(plot_df, x="Date", y="Units", color="Type", markers=True,
                  color_discrete_map={"Historical usage": "#167D9A", "Baseline forecast": "#E7A23B"})
    fig.update_layout(margin=dict(t=20,b=10,l=10,r=10), legend_title_text="", yaxis_title="Units used")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("#### Forecast interpretation")
    if med_row["Stock"] < demand_total:
        st.warning(f"Current stock is lower than the estimated {horizon}-day demand. Review replenishment and supplier lead time.")
    else:
        st.info(f"Current stock is above the estimated {horizon}-day demand, but still review lead time, safety stock and expiry.")
    st.caption("Method: weighted average of recent 7-day and selected-period usage, with a small capped trend adjustment. This is a transparent baseline, not a trained or clinically validated AI model.")

elif page == "Stock Risk & Reorder":
    st.subheader("Stock-risk alerts & reorder recommendations")
    st.markdown('<p class="section-sub">Prioritize inventory review using current stock, average usage, supplier lead time and safety stock.</p>', unsafe_allow_html=True)

    risk = inventory.copy()
    risk["Risk reason"] = risk.apply(
        lambda r: "Stock may not cover supplier lead time" if r["Stock"] <= r["Lead-time Demand"]
        else ("At/below safety stock or low days of cover" if r["Status"] == "Low" else "No immediate rule-based alert"),
        axis=1
    )
    critical = risk[risk["Status"] == "Critical"]
    low = risk[risk["Status"] == "Low"]
    a, b, c = st.columns(3)
    a.metric("Critical", len(critical))
    b.metric("Low", len(low))
    c.metric("Healthy", int((risk["Status"] == "Healthy").sum()))

    if len(critical):
        st.error("Critical: review these items first.")
        st.dataframe(critical[["Medicine", "Stock", "Daily Usage", "Lead Time (days)", "Lead-time Demand", "Days of Cover", "Risk reason", "Suggested Reorder"]], hide_index=True, use_container_width=True)
    if len(low):
        st.warning("Low stock: plan a replenishment review.")
        st.dataframe(low[["Medicine", "Stock", "Daily Usage", "Lead Time (days)", "Safety Stock", "Days of Cover", "Risk reason", "Suggested Reorder"]], hide_index=True, use_container_width=True)
    if not len(critical) and not len(low):
        st.success("No stock-risk alerts for the selected filters.")

    st.markdown("#### Reorder recommendations")
    st.write("Suggested quantity uses a simple target: expected demand during lead time plus 7 days of cover and safety stock, minus current stock. Confirm supplier constraints and expiry before ordering.")
    reorder = risk[risk["Suggested Reorder"] > 0].sort_values("Suggested Reorder", ascending=False)
    st.dataframe(reorder[["Medicine", "Supplier", "Stock", "Daily Usage", "Lead Time (days)", "Safety Stock", "Suggested Reorder", "Unit Cost (₹)"]], hide_index=True, use_container_width=True)
    if not reorder.empty:
        reorder["Estimated order cost (₹)"] = reorder["Suggested Reorder"] * reorder["Unit Cost (₹)"]
        st.metric("Estimated cost of suggested replenishment", f"₹{reorder['Estimated order cost (₹)'].sum():,.2f}")
        st.download_button("⬇️ Download reorder recommendations", data=reorder.to_csv(index=False).encode("utf-8"),
                           file_name="medstock_reorder_recommendations.csv", mime="text/csv")

st.markdown("---")
st.caption("MedStock AI • DATA THIRAN prototype • Demonstration only. Forecasts and reorder quantities are simplified estimates; verify with qualified pharmacy/hospital staff before real-world use.")
