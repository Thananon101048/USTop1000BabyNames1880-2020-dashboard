import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Twitch Streamers Dashboard",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Top 1000 Twitch Streamers Dashboard (May 2024)")
st.markdown("Interactive Dashboard สำหรับวิเคราะห์ข้อมูล Top Twitch Streamers")

# ===============================
# Upload CSV
# ===============================
uploaded_file = st.file_uploader("📂 Upload Twitch CSV File", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("📄 ข้อมูลทั้งหมด")
    st.dataframe(df)

    # ===============================
    # Sidebar Filters
    # ===============================
    st.sidebar.header("🔎 Filters")

    # Filter by game
    if "game_name" in df.columns:
        games = df["game_name"].unique()
        selected_games = st.sidebar.multiselect(
            "เลือกเกม",
            games,
            default=games
        )
        df = df[df["game_name"].isin(selected_games)]

    # Filter by country
    if "country" in df.columns:
        countries = df["country"].unique()
        selected_countries = st.sidebar.multiselect(
            "เลือกประเทศ",
            countries,
            default=countries
        )
        df = df[df["country"].isin(selected_countries)]

    # ===============================
    # Top 10 by Followers
    # ===============================
    st.subheader("🏆 Top 10 by Followers")

    if "followers" in df.columns:
        top_followers = df.sort_values(by="followers", ascending=False).head(10)

        fig1 = px.bar(
            top_followers,
            x="followers",
            y="user_name",
            orientation="h",
            text="followers",
            title="Top 10 Twitch Streamers by Followers"
        )
        fig1.update_traces(textposition="outside")
        st.plotly_chart(fig1, use_container_width=True)

    # ===============================
    # Top 10 by Average Viewers
    # ===============================
    st.subheader("📈 Top 10 by Average Viewers")

    if "avg_viewers" in df.columns:
        top_viewers = df.sort_values(by="avg_viewers", ascending=False).head(10)

        fig2 = px.bar(
            top_viewers,
            x="avg_viewers",
            y="user_name",
            orientation="h",
            text="avg_viewers",
            title="Top 10 Twitch Streamers by Avg Viewers"
        )
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

    # ===============================
    # Trend Chart (Followers vs Views)
    # ===============================
    st.subheader("📊 Followers vs Avg Viewers")

    if "followers" in df.columns and "avg_viewers" in df.columns:
        fig3 = px.scatter(
            df,
            x="followers",
            y="avg_viewers",
            hover_data=["user_name", "game_name"],
            title="Followers vs Avg Viewers"
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ===============================
    # Download Filtered Data
    # ===============================
    st.subheader("⬇ Download Data")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_twitch_streamers.csv",
        mime="text/csv"
    )

else:
    st.info("📂 กรุณาอัปโหลดไฟล์ CSV เพื่อเริ่มใช้งาน")
