import streamlit as st
import pandas as pd
import plotly.express as px

# 📌 Fungsi format Rupiah
def format_rupiah(value):
    try:
        return f"Rp. {value:,.0f}".replace(",", ".")
    except:
        return "Rp. 0"

# 🚀 Load data
df = pd.read_csv("data_kendaraan.csv")  # Ganti dengan path file kamu

# 🧼 Validasi kolom
required_columns = ["KECAMATAN", "KELURAHAN", "RT", "JUMLAH_KENDARAAN", "POKOK_PKB"]
missing = [col for col in required_columns if col not in df.columns]
if missing:
    st.error(f"Kolom berikut tidak ditemukan di data: {missing}")
    st.stop()

# 🧮 Total Pokok PKB keseluruhan
total_pkb = df["POKOK_PKB"].sum()
st.title("📊 Dashboard Analisis PKB")
st.markdown(f"### 💰 Total Pokok PKB Keseluruhan: **{format_rupiah(total_pkb)}**")

# 📋 Sidebar filter
st.sidebar.header("🔍 Filter Data")

selected_kecamatan = st.sidebar.selectbox(
    "Pilih Kecamatan",
    sorted(df["KECAMATAN"].dropna().unique())
)

filtered_df = df[df["KECAMATAN"] == selected_kecamatan]

selected_kelurahan = st.sidebar.selectbox(
    "Pilih Kelurahan",
    sorted(filtered_df["KELURAHAN"].dropna().unique())
)

filtered_df = filtered_df[filtered_df["KELURAHAN"] == selected_kelurahan]

selected_rt = st.sidebar.selectbox(
    "Pilih RT",
    sorted(filtered_df["RT"].dropna().unique())
)

filtered_df = filtered_df[filtered_df["RT"] == selected_rt]

# 📊 Jumlah Kendaraan per Kecamatan
st.subheader("Jumlah Kendaraan per Kecamatan")
fig_kec_kendaraan = px.bar(
    df.groupby("KECAMATAN")["JUMLAH_KENDARAAN"].sum().reset_index(),
    x="KECAMATAN",
    y="JUMLAH_KENDARAAN",
    title="Jumlah Kendaraan per Kecamatan",
    color="JUMLAH_KENDARAAN"
)
st.plotly_chart(fig_kec_kendaraan, use_container_width=True)

# 📊 Pokok PKB per Kecamatan
st.subheader("Pokok PKB per Kecamatan")
fig_kec_pkb = px.bar(
    df.groupby("KECAMATAN")["POKOK_PKB"].sum().reset_index(),
    x="KECAMATAN",
    y="POKOK_PKB",
    title="Total Pokok PKB per Kecamatan",
    color="POKOK_PKB"
)
fig_kec_pkb.update_layout(yaxis_tickformat=',', yaxis_title="Total Pokok PKB (Rp)")
fig_kec_pkb.update_traces(hovertemplate='Kecamatan: %{x}<br>Pokok PKB: Rp. %{y:,.0f}<extra></extra>')
st.plotly_chart(fig_kec_pkb, use_container_width=True)

# 📊 Jumlah Kendaraan per Kelurahan
st.subheader(f"Jumlah Kendaraan di Kecamatan {selected_kecamatan}")
fig_kel_kendaraan = px.bar(
    df[df["KECAMATAN"] == selected_kecamatan].groupby("KELURAHAN")["JUMLAH_KENDARAAN"].sum().reset_index(),
    x="KELURAHAN",
    y="JUMLAH_KENDARAAN",
    title="Jumlah Kendaraan per Kelurahan",
    color="JUMLAH_KENDARAAN"
)
st.plotly_chart(fig_kel_kendaraan, use_container_width=True)

# 📊 Pokok PKB per Kelurahan
st.subheader(f"Pokok PKB di Kecamatan {selected_kecamatan}")
fig_kel_pkb = px.bar(
    df[df["KECAMATAN"] == selected_kecamatan].groupby("KELURAHAN")["POKOK_PKB"].sum().reset_index(),
    x="KELURAHAN",
    y="POKOK_PKB",
    title="Total Pokok PKB per Kelurahan",
    color="POKOK_PKB"
)
fig_kel_pkb.update_layout(yaxis_tickformat=',', yaxis_title="Total Pokok PKB (Rp)")
fig_kel_pkb.update_traces(hovertemplate='Kelurahan: %{x}<br>Pokok PKB: Rp. %{y:,.0f}<extra></extra>')
st.plotly_chart(fig_kel_pkb, use_container_width=True)

# 📊 Jumlah Kendaraan per RT
st.subheader(f"Jumlah Kendaraan di Kelurahan {selected_kelurahan}")
fig_rt_kendaraan = px.bar(
    df[(df["KECAMATAN"] == selected_kecamatan) & (df["KELURAHAN"] == selected_kelurahan)].groupby("RT")["JUMLAH_KENDARAAN"].sum().reset_index(),
    x="RT",
    y="JUMLAH_KENDARAAN",
    title="Jumlah Kendaraan per RT",
    color="JUMLAH_KENDARAAN"
)
st.plotly_chart(fig_rt_kendaraan, use_container_width=True)

# 📊 Pokok PKB per RT
st.subheader(f"Pokok PKB di Kelurahan {selected_kelurahan}")
fig_rt_pkb = px.bar(
    df[(df["KECAMATAN"] == selected_kecamatan) & (df["KELURAHAN"] == selected_kelurahan)].groupby("RT")["POKOK_PKB"].sum().reset_index(),
    x="RT",
    y="POKOK_PKB",
    title="Total Pokok PKB per RT",
    color="POKOK_PKB"
)
fig_rt_pkb.update_layout(yaxis_tickformat=',', yaxis_title="Total Pokok PKB (Rp)")
fig_rt_pkb.update_traces(hovertemplate='RT: %{x}<br>Pokok PKB: Rp. %{y:,.0f}<extra></extra>')
st.plotly_chart(fig_rt_pkb, use_container_width=True)

# 📄 Tampilkan data terfilter
st.subheader("📄 Data Terfilter")
filtered_df["POKOK_PKB_RUPIAH"] = filtered_df["POKOK_PKB"].apply(format_rupiah)
st.dataframe(filtered_df[["KECAMATAN", "KELURAHAN", "RT", "JUMLAH_KENDARAAN", "POKOK_PKB_RUPIAH"]])