import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

df = pd.read_csv("Metro_Interstate_Traffic_Volume.csv")

st.title("Traffic Volume Dashboard")

st.dataframe(df.head()) # show all data in a table

df['date_time'] = pd.to_datetime(df['date_time'])

day = df.copy()[(df['date_time'].dt.hour >= 7) | (df['date_time'].dt.hour < 19)]

night = df.copy()[(df['date_time'].dt.hour >= 19) | (df['date_time'].dt.hour < 7)]

# Create bar charts with altair to display on streamlit

day_chart = (
    alt.Chart(day)
    .mark_bar()
    .encode(
        alt.X("traffic_volume:Q", 
            bin=alt.Bin(maxbins=30),
            scale=alt.Scale(domain=[-100, 7500]),
            title="Traffic Volume"),
        alt.Y("count()", scale=alt.Scale(domain=[0, 8000]), title="Frequency"),
    )
    .properties(title="Traffic Volume Distribution (Day)")
)

night_chart = (
    alt.Chart(night)
    .mark_bar()
    .encode(
        alt.X("traffic_volume:Q", 
            bin=alt.Bin(maxbins=30),
            scale=alt.Scale(domain=[-100, 7500]),
            title="Traffic Volume"),
        alt.Y("count()", scale=alt.Scale(domain=[0, 8000]), title="Frequency"),
    )
    .properties(title="Traffic Volume Distribution (Night)")
)

col1, col2 = st.columns(2)

with col1:
    st.altair_chart(day_chart, width="stretch")

with col2:
    st.altair_chart(night_chart, width="stretch")
    
# Create line graph

day["month"] = day["date_time"].dt.month
by_month = day.groupby("month").mean(numeric_only=True).reset_index()

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

by_month_chart = (
    alt.Chart(by_month)
    .mark_line(point=True)
    .encode(
        alt.X(
            "month:O",
            title="Month",
            axis=alt.Axis(labelExpr=f"{months}[datum.value - 1]")
            ),
        alt.Y(
            "traffic_volume:Q",
            title="Average Traffic Volume"),
    )
    .properties(title="Traffic Volume by Month")
)

with st.container(horizontal_alignment="center"):
    st.altair_chart(by_month_chart, width="stretch")
    
    
# Create scatterplot

day["dayofweek"] = day["date_time"].dt.dayofweek
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

temp_and_day_chart = (
    alt.Chart(day)
    .mark_circle(size=60)
    .encode(
        x=alt.X("traffic_volume", title="Traffic Volume"),
        y=alt.Y("temp", title="Temperature"),
        color=alt.Color(
            "dayofweek:O",
            title="Day of Week",
            scale=alt.Scale(range=["#ff0000", "#e65656", "#D87878", "#d99c9c", "#dbb9b9", "#694038", "#280808"]),
            legend=alt.Legend(labelExpr=f"{days}[datum.value]"),
        ),
    )
)

with st.container(horizontal_alignment="center"):
    st.altair_chart(temp_and_day_chart, width="stretch")
    
