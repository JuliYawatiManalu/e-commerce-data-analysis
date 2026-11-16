
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# KONFIGURASI DASHBOARD
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛍️",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# MEMUAT DATASET
@st.cache_data
def load_data():

    orders_df = pd.read_csv(
        DATA_DIR / "orders_dataset.csv"
    )

    order_items_df = pd.read_csv(
        DATA_DIR / "order_items_dataset.csv"
    )

    products_df = pd.read_csv(
        DATA_DIR / "products_dataset.csv"
    )

    category_df = pd.read_csv(
        DATA_DIR / "product_category_name_translation.csv"
    )

    payments_df = pd.read_csv(
        DATA_DIR / "order_payments_dataset.csv"
    )

    customers_df = pd.read_csv(
        DATA_DIR / "customers_dataset.csv"
    )

    return (
        orders_df,
        order_items_df,
        products_df,
        category_df,
        payments_df,
        customers_df
    )


try:
    (
        orders_df,
        order_items_df,
        products_df,
        category_df,
        payments_df,
        customers_df
    ) = load_data()

except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.stop()


# DATA CLEANING SESUAI NOTEBOOK
orders_clean = orders_df.copy()
order_items_clean = order_items_df.copy()
products_clean = products_df.copy()
category_clean = category_df.copy()
payments_clean = payments_df.copy()

customers_clean = customers_df.copy()

# Mengubah kolom tanggal menjadi datetime
order_date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in order_date_columns:
    orders_clean[column] = pd.to_datetime(
        orders_clean[column],
        errors="coerce"
    )

order_items_clean["shipping_limit_date"] = pd.to_datetime(
    order_items_clean["shipping_limit_date"],
    errors="coerce"
)

# Mengisi kategori produk yang kosong
products_clean["product_category_name"] = (
    products_clean["product_category_name"].fillna("Unknown")
)

# Menggabungkan produk dengan terjemahan kategori
products_clean = products_clean.merge(
    category_clean,
    on="product_category_name",
    how="left"
)


# DATA CLEANING SESUAI NOTEBOOK
orders_clean = orders_df.copy()
order_items_clean = order_items_df.copy()
products_clean = products_df.copy()
category_clean = category_df.copy()
payments_clean = payments_df.copy()
customers_clean = customers_df.copy()

# Mengubah kolom tanggal menjadi datetime
order_date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in order_date_columns:
    orders_clean[column] = pd.to_datetime(
        orders_clean[column],
        errors="coerce"
    )

order_items_clean["shipping_limit_date"] = pd.to_datetime(
    order_items_clean["shipping_limit_date"],
    errors="coerce"
)


# JUDUL DAN DESKRIPSI DASHBOARD
st.title("🛍️ E-Commerce Dashboard")

st.markdown("""
Dashboard ini menyajikan hasil analisis data e-commerce Olist
untuk memahami pendapatan produk, penggunaan metode pembayaran,
karakteristik transaksi, dan segmentasi pelanggan.
""")

st.divider()


# DATASET OVERVIEW
st.header("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Orders",
        f"{len(orders_clean):,}"
    )

with col2:
    st.metric(
        "Total Order Items",
        f"{len(order_items_clean):,}"
    )

with col3:
    st.metric(
        "Total Customers",
        f"{customers_clean['customer_unique_id'].nunique():,}"
    )

dataset_info = pd.DataFrame({
    "Dataset": [
        "Orders",
        "Order Items",
        "Products",
        "Category Translation",
        "Order Payments",
        "Customers"
    ],
    "Rows": [
        len(orders_clean),
        len(order_items_clean),
        len(products_clean),
        len(category_clean),
        len(payments_clean),
        len(customers_clean)
    ]
})

with st.expander("Lihat informasi dataset"):
    st.dataframe(
        dataset_info,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# BUSINESS QUESTION 1
# ANALISIS PENDAPATAN PRODUK

st.header("1. Analisis Pendapatan Produk")

st.markdown("""
**Business Question 1**

Kategori produk mana yang menyumbang pendapatan terbesar
pada Januari-Agustus 2018, dan bagaimana pertumbuhannya
dibandingkan periode Januari-Agustus 2017?
""")


# Menyeleksi pesanan delivered Januari-Agustus 2017 dan 2018
orders_bq1 = orders_clean[
    (orders_clean["order_status"] == "delivered") &
    (orders_clean["order_purchase_timestamp"].dt.year.isin([2017, 2018])) &
    (orders_clean["order_purchase_timestamp"].dt.month <= 8)
].copy()


# Menggabungkan data pesanan dengan item produk
items_bq1 = orders_bq1.merge(
    order_items_clean,
    on="order_id",
    how="inner"
)


# Menggabungkan informasi kategori produk
items_bq1 = items_bq1.merge(
    products_clean[
        ["product_id", "product_category_name_english"]
    ],
    on="product_id",
    how="left"
)


# Membuat kolom tahun dan bulan
items_bq1["year"] = (
    items_bq1["order_purchase_timestamp"].dt.year
)

items_bq1["month"] = (
    items_bq1["order_purchase_timestamp"].dt.month
)


# RINGKASAN PENDAPATAN
revenue_by_year = (
    items_bq1.groupby("year")
    .agg(
        total_revenue=("price", "sum"),
        total_items=("order_item_id", "count"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

revenue_2017 = revenue_by_year.loc[
    revenue_by_year["year"] == 2017,
    "total_revenue"
].iloc[0]

revenue_2018 = revenue_by_year.loc[
    revenue_by_year["year"] == 2018,
    "total_revenue"
].iloc[0]

growth = (
    (revenue_2018 - revenue_2017) /
    revenue_2017
) * 100


# Menampilkan metrik pendapatan
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Pendapatan 2017",
        f"BRL {revenue_2017:,.2f}"
    )

with col2:
    st.metric(
        "Pendapatan 2018",
        f"BRL {revenue_2018:,.2f}"
    )

with col3:
    st.metric(
        "Pertumbuhan Pendapatan",
        f"{growth:.2f}%"
    )

# PENDAPATAN BERDASARKAN KATEGORI

category_revenue = (
    items_bq1.groupby(
        ["product_category_name_english", "year"]
    )["price"]
    .sum()
    .reset_index()
)

category_comparison = category_revenue.pivot(
    index="product_category_name_english",
    columns="year",
    values="price"
).fillna(0)

category_comparison = category_comparison.rename(
    columns={
        2017: "revenue_2017",
        2018: "revenue_2018"
    }
)

category_comparison["contribution_2018 (%)"] = (
    category_comparison["revenue_2018"] /
    revenue_2018 * 100
)

category_comparison["growth (%)"] = (
    (
        category_comparison["revenue_2018"] -
        category_comparison["revenue_2017"]
    ) /
    category_comparison["revenue_2017"].replace(0, np.nan)
) * 100

category_comparison = category_comparison.sort_values(
    by="revenue_2018",
    ascending=False
)

top_10_categories = (
    category_comparison[
        [
            "revenue_2017",
            "revenue_2018",
            "contribution_2018 (%)",
            "growth (%)"
        ]
    ]
    .head(10)
)


# VISUALISASI 1
# TOP 10 KATEGORI PRODUK
st.subheader("10 Kategori Produk dengan Pendapatan Terbesar")

plot_top_10 = (
    top_10_categories
    .reset_index()
    .sort_values("revenue_2018", ascending=True)
)

fig1 = px.bar(
    plot_top_10,
    x="revenue_2018",
    y="product_category_name_english",
    orientation="h",
    text="revenue_2018",
    labels={
        "revenue_2018": "Pendapatan (BRL)",
        "product_category_name_english": "Kategori Produk"
    },
    title="Top 10 Kategori Produk (Januari-Agustus 2018)"
)

fig1.update_traces(
    marker_color="#2A6F97",
    texttemplate="BRL %{x:,.0f}",
    textposition="outside"
)

fig1.update_layout(
    height=550,
    yaxis_title="",
    xaxis_title="Pendapatan (BRL)",
    showlegend=False
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# VISUALISASI 2
# TREN PENDAPATAN BULANAN
st.subheader("Tren Pendapatan Produk Bulanan")

monthly_revenue = (
    items_bq1.groupby(["year", "month"])
    .agg(
        total_revenue=("price", "sum"),
        total_orders=("order_id", "nunique"),
        total_items=("order_item_id", "count")
    )
    .reset_index()
)

monthly_revenue["period"] = (
    monthly_revenue["year"].astype(str) + "-" +
    monthly_revenue["month"].astype(str).str.zfill(2)
)

monthly_revenue = monthly_revenue.sort_values(
    by=["year", "month"]
)

monthly_revenue_pivot = monthly_revenue.pivot(
    index="month",
    columns="year",
    values="total_revenue"
)

monthly_revenue_plot = (
    monthly_revenue.reset_index(drop=True)
)

fig2 = px.line(
    monthly_revenue_plot,
    x="month",
    y="total_revenue",
    color="year",
    markers=True,
    labels={
        "month": "Bulan",
        "total_revenue": "Pendapatan (BRL)",
        "year": "Tahun"
    },
    title="Perbandingan Pendapatan Bulanan 2017 dan 2018"
)

fig2.update_xaxes(
    tickmode="array",
    tickvals=list(range(1, 9)),
    ticktext=[
        "Jan", "Feb", "Mar", "Apr",
        "Mei", "Jun", "Jul", "Agu"
    ]
)

fig2.update_layout(
    height=500,
    yaxis_title="Pendapatan (BRL)",
    xaxis_title="Bulan",
    legend_title="Tahun"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# TABEL RINGKASAN KATEGORI
with st.expander("Lihat detail pendapatan 10 kategori teratas"):

    category_display = (
        top_10_categories
        .reset_index()
        .rename(columns={
            "product_category_name_english": "Kategori Produk",
            "revenue_2017": "Pendapatan 2017",
            "revenue_2018": "Pendapatan 2018",
            "contribution_2018 (%)": "Kontribusi 2018 (%)",
            "growth (%)": "Pertumbuhan (%)"
        })
    )

    st.dataframe(
        category_display.round(2),
        use_container_width=True,
        hide_index=True
    )
    
    
# 2. ANALISIS METODE PEMBAYARAN (BQ2)
st.divider()

st.header("2. Analisis Metode Pembayaran")

st.markdown("**Business Question 2**")

st.write(
    "Bagaimana komposisi dan tren penggunaan metode pembayaran pelanggan "
    "setiap bulan, serta bagaimana perbedaan rata-rata nilai pembayaran "
    "dan jumlah cicilan berdasarkan metode pembayaran selama "
    "Januari 2017 hingga Agustus 2018?"
)

# Memilih seluruh pesanan pada periode Januari 2017 - Agustus 2018
orders_bq2 = orders_clean[
    (orders_clean["order_purchase_timestamp"] >= "2017-01-01") &
    (orders_clean["order_purchase_timestamp"] < "2018-09-01")
].copy()

# Menggabungkan data pesanan dengan data pembayaran
payments_bq2 = orders_bq2.merge(
    payments_clean,
    on="order_id",
    how="inner"
)

# Membuat kolom tahun, bulan, dan periode
payments_bq2["year"] = (
    payments_bq2["order_purchase_timestamp"].dt.year
)

payments_bq2["month"] = (
    payments_bq2["order_purchase_timestamp"].dt.month
)

payments_bq2["period"] = (
    payments_bq2["order_purchase_timestamp"].dt.strftime("%Y-%m")
)

# Mengecualikan metode pembayaran not_defined
payments_method_bq2 = payments_bq2[
    payments_bq2["payment_type"] != "not_defined"
].copy()

# Menghitung jumlah pesanan unik berdasarkan metode pembayaran
payment_method_summary = (
    payments_method_bq2.groupby("payment_type")
    .agg(
        total_orders=("order_id", "nunique"),
        total_payment_records=("order_id", "count"),
        total_payment_value=("payment_value", "sum")
    )
    .reset_index()
)

# Menghitung persentase pesanan setiap metode
total_orders_bq2 = orders_bq2["order_id"].nunique()

payment_method_summary["order_percentage (%)"] = (
    payment_method_summary["total_orders"] /
    total_orders_bq2 * 100
)

payment_method_summary = payment_method_summary.sort_values(
    by="total_orders",
    ascending=False
)

# Menghitung tren penggunaan metode pembayaran setiap bulan
monthly_payment_usage = (
    payments_method_bq2.groupby(
        ["period", "payment_type"]
    )["order_id"]
    .nunique()
    .reset_index(name="total_orders")
)

monthly_payment_pivot = monthly_payment_usage.pivot(
    index="period",
    columns="payment_type",
    values="total_orders"
).fillna(0)

monthly_payment_pivot = monthly_payment_pivot.sort_index()

# Menghitung rata-rata nilai pembayaran
payment_value_summary = (
    payments_method_bq2.groupby("payment_type")
    .agg(
        total_payment_records=("payment_value", "count"),
        total_payment_value=("payment_value", "sum"),
        average_payment_value=("payment_value", "mean")
    )
    .reset_index()
    .sort_values(
        by="average_payment_value",
        ascending=False
    )
)

# Menghitung rata-rata cicilan
# Data cicilan bernilai 0 dikecualikan
payments_installments_bq2 = payments_method_bq2[
    payments_method_bq2["payment_installments"] > 0
].copy()

installment_summary = (
    payments_installments_bq2.groupby("payment_type")
    .agg(
        total_payment_records=("payment_installments", "count"),
        average_installments=("payment_installments", "mean")
    )
    .reset_index()
    .sort_values(
        by="average_installments",
        ascending=False
    )
)

# VISUALISASI BQ2
st.subheader("Ringkasan Penggunaan Metode Pembayaran")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Pesanan",
        f"{total_orders_bq2:,}"
    )

with col2:
    st.metric(
        "Total Catatan Pembayaran",
        f"{len(payments_bq2):,}"
    )

with col3:
    st.metric(
        "Jumlah Metode Pembayaran",
        f"{payments_method_bq2['payment_type'].nunique()}"
    )

st.caption(
    "Analisis mencakup seluruh status pesanan. "
    "Pesanan yang menggunakan lebih dari satu metode pembayaran "
    "dapat terhitung pada lebih dari satu kategori metode."
)

# Grafik 1: Komposisi metode pembayaran
st.subheader("Komposisi Penggunaan Metode Pembayaran")

fig_payment_method = px.bar(
    payment_method_summary.sort_values(
        "total_orders",
        ascending=True
    ),
    x="total_orders",
    y="payment_type",
    orientation="h",
    text="total_orders",
    labels={
        "total_orders": "Jumlah Pesanan Unik",
        "payment_type": "Metode Pembayaran"
    }
)

fig_payment_method.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_payment_method.update_layout(
    xaxis_title="Jumlah Pesanan Unik",
    yaxis_title="Metode Pembayaran"
)

st.plotly_chart(
    fig_payment_method,
    use_container_width=True
)

# Grafik 2: Tren penggunaan metode pembayaran bulanan
st.subheader("Tren Penggunaan Metode Pembayaran Bulanan")

monthly_payment_chart = (
    monthly_payment_pivot
    .reset_index()
    .melt(
        id_vars="period",
        var_name="payment_type",
        value_name="total_orders"
    )
)

fig_monthly_payment = px.line(
    monthly_payment_chart,
    x="period",
    y="total_orders",
    color="payment_type",
    markers=True,
    labels={
        "period": "Bulan",
        "total_orders": "Jumlah Pesanan Unik",
        "payment_type": "Metode Pembayaran"
    }
)

fig_monthly_payment.update_layout(
    xaxis_title="Bulan",
    yaxis_title="Jumlah Pesanan Unik",
    legend_title="Metode Pembayaran"
)

st.plotly_chart(
    fig_monthly_payment,
    use_container_width=True
)

# Grafik 3: Rata-rata nilai pembayaran
st.subheader("Rata-rata Nilai Pembayaran Berdasarkan Metode")

fig_payment_value = px.bar(
    payment_value_summary.sort_values(
        "average_payment_value",
        ascending=True
    ),
    x="average_payment_value",
    y="payment_type",
    orientation="h",
    text="average_payment_value",
    labels={
        "average_payment_value": "Rata-rata Pembayaran (BRL)",
        "payment_type": "Metode Pembayaran"
    }
)

fig_payment_value.update_traces(
    texttemplate="BRL %{text:,.2f}",
    textposition="outside"
)

fig_payment_value.update_layout(
    xaxis_title="Rata-rata Nilai Pembayaran (BRL)",
    yaxis_title="Metode Pembayaran"
)

st.plotly_chart(
    fig_payment_value,
    use_container_width=True
)

# Grafik 4: Rata-rata jumlah cicilan
st.subheader("Rata-rata Jumlah Cicilan Berdasarkan Metode")

fig_installment = px.bar(
    installment_summary.sort_values(
        "average_installments",
        ascending=True
    ),
    x="payment_type",
    y="average_installments",
    text="average_installments",
    labels={
        "average_installments": "Rata-rata Jumlah Cicilan",
        "payment_type": "Metode Pembayaran"
    }
)

fig_installment.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig_installment.update_layout(
    xaxis_title="Metode Pembayaran",
    yaxis_title="Rata-rata Jumlah Cicilan"
)

st.plotly_chart(
    fig_installment,
    use_container_width=True
)

# Tabel detail
with st.expander("Lihat detail ringkasan metode pembayaran"):
    st.write("Komposisi metode pembayaran")
    st.dataframe(
        payment_method_summary.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.write("Rata-rata nilai pembayaran")
    st.dataframe(
        payment_value_summary.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.write("Rata-rata jumlah cicilan")
    st.dataframe(
        installment_summary.round(2),
        use_container_width=True,
        hide_index=True
    )
    
    
# 3. ADVANCED ANALYSIS: BINNING & MANUAL GROUPING

st.divider()

st.header("3. Advanced Analysis")
st.subheader("3.1 Binning dan Manual Grouping")

st.write(
    "Analisis ini mengelompokkan pesanan berdasarkan total nilai pembayaran "
    "untuk melihat pola penggunaan metode pembayaran dan cicilan."
)

# A. BINNING NILAI TRANSAKSI

# Menggabungkan catatan pembayaran menjadi satu baris per pesanan
order_payment = (
    payments_method_bq2.groupby("order_id")
    .agg(
        total_payment=("payment_value", "sum"),
        payment_methods=("payment_type", lambda x: list(x.unique()))
    )
    .reset_index()
)

# Mengelompokkan metode pembayaran
order_payment["payment_method_group"] = (
    order_payment["payment_methods"].apply(
        lambda x: x[0] if len(x) == 1 else "multi_method"
    )
)

# Menentukan rentang nilai transaksi
value_bins = [0, 50, 100, 200, 500, float("inf")]

value_labels = [
    "< R$50",
    "R$50 - 100",
    "R$100 - 200",
    "R$200 - 500",
    "> R$500"
]

order_payment["value_bin"] = pd.cut(
    order_payment["total_payment"],
    bins=value_bins,
    labels=value_labels,
    right=False
)

# Menghitung jumlah dan total nilai transaksi per kelompok
value_group_summary = (
    order_payment.groupby("value_bin", observed=False)
    .agg(
        total_orders=("order_id", "count"),
        total_payment=("total_payment", "sum")
    )
    .reset_index()
)

value_group_summary["order_percentage"] = (
    value_group_summary["total_orders"] /
    value_group_summary["total_orders"].sum() * 100
)

value_group_summary["payment_percentage"] = (
    value_group_summary["total_payment"] /
    value_group_summary["total_payment"].sum() * 100
)

# B. MANUAL GROUPING METODE PEMBAYARAN

method_by_value = pd.crosstab(
    order_payment["value_bin"],
    order_payment["payment_method_group"],
    normalize="index"
) * 100

method_by_value = method_by_value.reindex(value_labels)

# C. MANUAL GROUPING JUMLAH CICILAN

# Mengambil pesanan yang menggunakan kartu kredit
credit_card_orders = (
    payments_method_bq2[
        payments_method_bq2["payment_type"] == "credit_card"
    ]
    .groupby("order_id")
    .agg(
        card_payment_value=("payment_value", "sum"),
        installments=("payment_installments", "max")
    )
    .reset_index()
)

# Mengelompokkan jumlah cicilan
credit_card_orders["installment_group"] = pd.cut(
    credit_card_orders["installments"],
    bins=[0, 1, 6, float("inf")],
    labels=["1x", "2-6x", ">6x"]
)

# Mengelompokkan nilai pembayaran kartu kredit
credit_card_orders["value_bin"] = pd.cut(
    credit_card_orders["card_payment_value"],
    bins=value_bins,
    labels=value_labels,
    right=False
)

# Membuat tabel persentase kelompok cicilan berdasarkan nilai transaksi
installment_by_value = pd.crosstab(
    credit_card_orders["value_bin"],
    credit_card_orders["installment_group"],
    normalize="index"
) * 100

installment_by_value = installment_by_value.reindex(value_labels)

# VISUALISASI BINNING DAN MANUAL GROUPING
# Grafik 1: Distribusi nilai transaksi
st.subheader("Distribusi Pesanan Berdasarkan Nilai Transaksi")

fig_value_distribution = px.bar(
    value_group_summary,
    x="value_bin",
    y="total_orders",
    text="total_orders",
    labels={
        "value_bin": "Rentang Nilai Transaksi",
        "total_orders": "Jumlah Pesanan"
    }
)

fig_value_distribution.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_value_distribution.update_layout(
    xaxis_title="Rentang Nilai Transaksi (BRL)",
    yaxis_title="Jumlah Pesanan"
)

st.plotly_chart(
    fig_value_distribution,
    use_container_width=True
)

# Grafik 2: Hubungan nilai transaksi dan metode pembayaran
st.subheader("Komposisi Metode Pembayaran pada Setiap Rentang Transaksi")

fig_method_heatmap = px.imshow(
    method_by_value,
    text_auto=".1f",
    aspect="auto",
    color_continuous_scale="Blues",
    labels={
        "x": "Metode Pembayaran",
        "y": "Rentang Nilai Transaksi",
        "color": "Persentase (%)"
    }
)

st.plotly_chart(
    fig_method_heatmap,
    use_container_width=True
)

# Grafik 3: Hubungan nilai transaksi dan jumlah cicilan
st.subheader("Pola Cicilan Kartu Kredit Berdasarkan Nilai Transaksi")

fig_installment_heatmap = px.imshow(
    installment_by_value,
    text_auto=".1f",
    aspect="auto",
    color_continuous_scale="Blues",
    labels={
        "x": "Kelompok Cicilan",
        "y": "Rentang Nilai Transaksi",
        "color": "Persentase (%)"
    }
)

st.plotly_chart(
    fig_installment_heatmap,
    use_container_width=True
)

# TABEL DETAIL
with st.expander("Lihat detail hasil Binning dan Manual Grouping"):

    st.write("Ringkasan nilai transaksi")
    st.dataframe(
        value_group_summary.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.write("Komposisi metode pembayaran berdasarkan nilai transaksi (%)")
    st.dataframe(
        method_by_value.round(2),
        use_container_width=True
    )

    st.write("Komposisi kelompok cicilan berdasarkan nilai transaksi (%)")
    st.dataframe(
        installment_by_value.round(2),
        use_container_width=True
    )


# 4. ADVANCED ANALYSIS: RFM ANALYSIS
st.divider()

st.subheader("3.2 RFM Analysis")

st.write(
    "RFM Analysis digunakan untuk mengelompokkan pelanggan berdasarkan "
    "waktu terakhir melakukan pembelian (Recency), frekuensi pembelian "
    "(Frequency), dan total nilai pembayaran (Monetary)."
)

# A. MENYIAPKAN DATA RFM

# Mengambil pesanan berstatus delivered pada periode analisis
orders_rfm = orders_clean[
    (orders_clean["order_status"] == "delivered") &
    (orders_clean["order_purchase_timestamp"] >= "2017-01-01") &
    (orders_clean["order_purchase_timestamp"] < "2018-09-01")
].copy()

# Menggabungkan data pesanan dengan identitas pelanggan
orders_rfm = orders_rfm.merge(
    customers_clean[["customer_id", "customer_unique_id"]],
    on="customer_id",
    how="left"
)

# Menghitung total pembayaran setiap pesanan
payment_per_order = (
    payments_clean.groupby("order_id")["payment_value"]
    .sum()
    .reset_index(name="order_payment")
)

orders_rfm = orders_rfm.merge(
    payment_per_order,
    on="order_id",
    how="left"
)

orders_rfm["order_payment"] = (
    orders_rfm["order_payment"].fillna(0)
)

# Menghitung Recency, Frequency, dan Monetary per pelanggan
reference_date = pd.Timestamp("2018-09-01")

rfm_summary = (
    orders_rfm.groupby("customer_unique_id")
    .agg(
        last_purchase=("order_purchase_timestamp", "max"),
        frequency=("order_id", "nunique"),
        monetary=("order_payment", "sum")
    )
    .reset_index()
)

rfm_summary["recency"] = (
    reference_date - rfm_summary["last_purchase"]
).dt.days

# B. MEMBUAT KELOMPOK RFM

# Kelompok Recency
rfm_summary["recency_group"] = pd.cut(
    rfm_summary["recency"],
    bins=[-1, 90, 180, 365, float("inf")],
    labels=["0-90 hari", "91-180 hari", "181-365 hari", ">365 hari"]
)

# Kelompok Frequency
def frequency_group(value):
    if value == 1:
        return "1 kali"
    elif value <= 3:
        return "2-3 kali"
    else:
        return ">3 kali"

rfm_summary["frequency_group"] = (
    rfm_summary["frequency"].apply(frequency_group)
)

# Kelompok Monetary berdasarkan kuantil
rfm_summary["monetary_group"] = pd.qcut(
    rfm_summary["monetary"],
    q=3,
    labels=["Low", "Medium", "High"],
    duplicates="drop"
)

# Batas 20% teratas untuk identifikasi Big Spender
monetary_80_percentile = rfm_summary["monetary"].quantile(0.80)

# C. SEGMENTASI PELANGGAN
def customer_segment(row):
    if row["frequency"] > 1 and row["recency"] <= 180:
        return "Loyal Aktif"

    elif row["frequency"] > 1 and row["recency"] > 180:
        return "Loyal Tidak Aktif"

    elif (
        row["monetary"] >= monetary_80_percentile
        and row["recency"] <= 180
    ):
        return "Big Spender"

    elif row["recency"] <= 90:
        return "Pelanggan Baru"

    elif row["recency"] <= 365:
        return "Perlu Reaktivasi"

    else:
        return "Hilang"

rfm_summary["customer_segment"] = (
    rfm_summary.apply(customer_segment, axis=1)
)

# D. RINGKASAN SEGMEN PELANGGAN
segment_order = [
    "Loyal Aktif",
    "Loyal Tidak Aktif",
    "Big Spender",
    "Pelanggan Baru",
    "Perlu Reaktivasi",
    "Hilang"
]

segment_summary = (
    rfm_summary.groupby("customer_segment")
    .agg(
        total_customers=("customer_unique_id", "count"),
        total_monetary=("monetary", "sum"),
        average_monetary=("monetary", "mean")
    )
    .reindex(segment_order)
    .fillna(0)
    .reset_index()
)

segment_summary["customer_percentage"] = (
    segment_summary["total_customers"] /
    segment_summary["total_customers"].sum() * 100
)

segment_summary["monetary_percentage"] = (
    segment_summary["total_monetary"] /
    segment_summary["total_monetary"].sum() * 100
)

# E. VISUALISASI RFM
st.markdown("### Ringkasan RFM")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Pelanggan",
        f"{rfm_summary['customer_unique_id'].nunique():,}"
    )

with col2:
    st.metric(
        "Pelanggan Berulang",
        f"{(rfm_summary['frequency'] > 1).sum():,}"
    )

with col3:
    st.metric(
        "Jumlah Segmen",
        f"{rfm_summary['customer_segment'].nunique()}"
    )

# Grafik 1: Distribusi pelanggan berdasarkan segmen
st.subheader("Distribusi Pelanggan Berdasarkan Segmen")

fig_rfm_customers = px.bar(
    segment_summary.sort_values(
        "total_customers",
        ascending=True
    ),
    x="total_customers",
    y="customer_segment",
    orientation="h",
    text="total_customers",
    labels={
        "total_customers": "Jumlah Pelanggan",
        "customer_segment": "Segmen Pelanggan"
    }
)

fig_rfm_customers.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_rfm_customers.update_layout(
    xaxis_title="Jumlah Pelanggan",
    yaxis_title="Segmen Pelanggan"
)

st.plotly_chart(
    fig_rfm_customers,
    use_container_width=True
)

# Grafik 2: Kontribusi pembayaran setiap segmen
st.subheader("Kontribusi Nilai Pembayaran Berdasarkan Segmen")

fig_rfm_monetary = px.bar(
    segment_summary.sort_values(
        "total_monetary",
        ascending=True
    ),
    x="total_monetary",
    y="customer_segment",
    orientation="h",
    text="total_monetary",
    labels={
        "total_monetary": "Total Pembayaran (BRL)",
        "customer_segment": "Segmen Pelanggan"
    }
)

fig_rfm_monetary.update_traces(
    texttemplate="BRL %{text:,.0f}",
    textposition="outside"
)

fig_rfm_monetary.update_layout(
    xaxis_title="Total Pembayaran (BRL)",
    yaxis_title="Segmen Pelanggan"
)

st.plotly_chart(
    fig_rfm_monetary,
    use_container_width=True
)

# Tabel detail segmen pelanggan
with st.expander("Lihat detail hasil RFM Analysis"):

    st.write("Ringkasan setiap segmen pelanggan")

    st.dataframe(
        segment_summary.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.write("Data RFM setiap pelanggan")

    st.dataframe(
        rfm_summary[
            [
                "customer_unique_id",
                "recency",
                "frequency",
                "monetary",
                "recency_group",
                "frequency_group",
                "monetary_group",
                "customer_segment"
            ]
        ].head(100),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Tabel data RFM menampilkan maksimal 100 pelanggan pertama."
    )