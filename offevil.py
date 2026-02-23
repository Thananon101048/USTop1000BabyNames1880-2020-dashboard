import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Baby Names Dashboard",
    page_icon="👶",
    layout="wide"
)

st.title("👶 US Top 1000 Baby Names (1880-2020)")
st.markdown("Interactive Dashboard สำหรับวิเคราะห์ชื่อเด็กยอดนิยม")

# =========================
# Upload file
# =========================
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file:

    # อ่านไฟล์ CSV
    df = pd.read_csv(uploaded_file)

    # แปลงปีให้เป็น int
    if "year" in df.columns:
        df["year"] = df["year"].astype(int)

    # Sidebar Filters
    st.sidebar.header("🔎 Filters")

    # เลือกช่วงปี
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    year_range = st.sidebar.slider(
        "Select year range",
        min_year,
        max_year,
        (min_year, max_year)
    )
    df = df[
        (df["year"] >= year_range[0]) &
        (df["year"] <= year_range[1])
    ]

    # เลือกเพศ
    if "gender" in df.columns:
        gender_list = df["gender"].unique()
        selected_gender = st.sidebar.multiselect(
            "Select gender",
            gender_list,
            default=gender_list
        )
        df = df[df["gender"].isin(selected_gender)]

    # =========================
    # Top 10 Names
    # =========================
    st.subheader("🏆 Top 10 Popular Names")

    # หา top 10 ตามจำนวน
    if "count" in df.columns:
        top10 = df.groupby("name")["count"].sum().reset_index()
        top10 = top10.sort_values(by="count", ascending=False).head(10)

        fig1 = px.bar(
            top10,
            x="name",
            y="count",
            text="count",
            title="Top 10 Most Popular Names"
        )
        fig1.update_traces(textposition="outside")
        st.plotly_chart(fig1, use_container_width=True)

    # =========================
    # Trend Chart
    # =========================
    st.subheader("📈 Name Trend Over Time")

    # ให้ผู้ใช้เลือกชื่อ
    all_names = df["name"].unique()
    selected_name = st.selectbox(
        "Select a name to view trend",
        all_names
    )

    trend_data = df[df["name"] == selected_name]
    fig2 = px.line(
        trend_data,
        x="year",
        y="count",
        title=f"Trend of {selected_name}"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # =========================
    # Raw Data Table
    # =========================
    st.subheader("📄 Raw Data")
    st.dataframe(df)

    # =========================
    # Download filtered data
    # =========================
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download Filtered Data",
        data=csv,
        file_name="filtered_baby_names.csv",
        mime="text/csv"
    )

else:
    st.info("📂 กรุณาอัปโหลดไฟล์ CSV เพื่อเริ่มใช้งาน")
