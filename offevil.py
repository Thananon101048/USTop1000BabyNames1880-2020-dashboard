import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Toyota Stock Dashboard",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Toyota Motors Stock Market Dashboard")
st.markdown("Interactive Dashboard สำหรับวิเคราะห์ข้อมูลราคาหุ้น Toyota")

# =============================
# Upload CSV
# =============================
uploaded_file = st.file_uploader("📂 Upload Toyota Stock CSV File", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # ถ้ามีคอลัมน์ Date -> แปลงเป็น datetime
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

    # =============================
    # Sidebar Filter
    # =============================
    st.sidebar.header("🔎 Filters")

    if "Date" in df.columns:
        min_date = df["Date"].min()
        max_date = df["Date"].max()

        date_range = st.sidebar.date_input(
            "Select Date Range",
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )

        df = df[
            (df["Date"] >= pd.to_datetime(date_range[0])) &
            (df["Date"] <= pd.to_datetime(date_range[1]))
        ]

    # =============================
    # Moving Averages
    # =============================
    if "Close" in df.columns:
        df["MA7"] = df["Close"].rolling(7).mean()
        df["MA30"] = df["Close"].rolling(30).mean()

    # =============================
    # KPI Section
    # =============================
    st.subheader("📌 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    if "High" in df.columns:
        col1.metric("Highest Price", f"${df['High'].max():.2f}")

    if "Low" in df.columns:
        col2.metric("Lowest Price", f"${df['Low'].min():.2f}")

    if "Close" in df.columns:
        col3.metric("Average Close", f"${df['Close'].mean():.2f}")

    if "Volume" in df.columns:
        col4.metric("Total Volume", f"{int(df['Volume'].sum()):,}")

    # =============================
    # Price Trend Chart
    # =============================
    st.subheader("📈 Price Trend with Moving Average")

    fig = go.Figure()

    if "Close" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode="lines",
            name="Close Price"
        ))

    if "MA7" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["MA7"],
            mode="lines",
            name="MA7"
        ))

    if "MA30" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["MA30"],
            mode="lines",
            name="MA30"
        ))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price ($)",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =============================
    # Volume Chart
    # =============================
    st.subheader("📊 Volume Analysis")

    if "Volume" in df.columns:
        fig2 = px.bar(
            df,
            x="Date",
            y="Volume",
            title="Trading Volume"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # =============================
    # Candlestick Chart
    # =============================
    st.subheader("🕯 Candlestick Chart")

    if all(col in df.columns for col in ["Open", "High", "Low", "Close"]):
        fig3 = go.Figure(data=[go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )])
        fig3.update_layout(
            xaxis_title="Date",
            yaxis_title="Price ($)"
        )
        st.plotly_chart(fig3, use_container_width=True)

    # =============================
    # Raw Data Table
    # =============================
    st.subheader("📄 Raw Data")
    st.dataframe(df)

    # =============================
    # Download Filtered Data
    # =============================
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download Filtered Data",
        data=csv,
        file_name="filtered_toyota_stock.csv",
        mime="text/csv"
    )

else:
    st.info("📂 กรุณาอัปโหลดไฟล์ CSV เพื่อเริ่มใช้งาน")
