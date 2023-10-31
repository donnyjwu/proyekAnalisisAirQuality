import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')


def rename_columns(df):
    df.rename(columns={
        "cnt": "total_users"
    }, inplace=True)


def replace_values(df):
    df.season.replace((1, 2, 3, 4), ('Spring', 'Summer', 'Fall', 'Winter'), inplace=True)
    df.weathersit.replace((1, 2, 3, 4), ('Clear', 'Misty', 'Light_rainsnow', 'Heavy_rainsnow'), inplace=True)
    df.weekday.replace((0, 1, 2, 3, 4, 5, 6),
                       ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'), inplace=True)


def create_users_df(df):
    rename_columns(df)
    replace_values(df)
    df = df.groupby(by="season").agg({
        "instant": "nunique",
        "casual": "mean",
        "registered": "mean",
        "total_users": "mean",
    })

    return df


def create_weather_sit_df(df):
    df = df.groupby(by="weathersit").agg({
        "total_users": "mean"
    })

    return df


def monthly_users_df(df):
    replace_values(df)
    df = df.groupby(by=["mnth"]).agg({
        "instant": "nunique",
        "total_users": "mean",
    }).sort_values(by="mnth", ascending=True)

    return df


def daily_users_df(df):
    replace_values(df)
    df = df.sort_values(by="dteday", ascending=True)

    return df


day_df = pd.read_csv("day.csv")

day_df.sort_values(by="dteday", inplace=True)
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan (meminjam logo Dicoding)
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu Pengguna Bike Sharing', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]

users_df = create_users_df(df)
weather_sit_df = create_weather_sit_df(df)
monthly_user_df = monthly_users_df(df)
daily_users_df = daily_users_df(df)

st.header('Proyek Analisis'
          ' Data Dashboard :sparkles:')

#This section is Total users of Bike Sharing based on Weather Situation
st.subheader('Jumlah Pengguna berdasarkan kondisi cuaca')

fig, ax = plt.subplots(figsize=(65, 35))

colors = ["#030bfc", "#fc6203", "#fc034e"]

sns.barplot(x="weathersit", y="total_users", data=weather_sit_df, palette=colors)
ax.set_ylabel(None)
ax.set_xlabel("Kondisi Cuaca", fontsize=30)
ax.set_title("Jumlah pengguna Bike Sharing berdasarkan kondisi cuaca", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader('Data jenis  pengguna Bike Sharing dan jumlahnya')
tab1, tab2, tab3 = st.tabs(["Jumlah pengguna rata-rata per musim", "Jumlah pengguna Casual per musim", "Jumlah pengguna Registered per musim"])

#This section is average users of each month
with tab1:
    st.header("Jumlah pengguna Casual dan Registered rata-rata per musim")
    fig, ax = plt.subplots(figsize=(65, 35))

    colors = ["#4287f5", "#030bfc", "#42f551", "#d742f5"]

    sns.barplot(x="season", y="total_users", data=users_df, palette=colors)
    ax.set_ylabel(None)
    ax.set_xlabel("Musim", fontsize=30)
    ax.set_title("Jumlah pengguna Bike Sharing rata-rata di setiap musim", loc="center", fontsize=50)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=30)

    st.pyplot(fig)

#This section is average casual users of each month
with tab2:
    st.header("Jumlah pengguna Casual rata-rata per musim")
    fig, ax = plt.subplots(figsize=(65, 35))

    colors = ["#4287f5", "#030bfc", "#42f551", "#d742f5"]

    sns.barplot(x="season", y="casual", data=users_df, palette=colors)
    ax.set_ylabel(None)
    ax.set_xlabel("Musim", fontsize=30)
    ax.set_title("Jumlah pengguna Bike Sharing Casual rata-rata di setiap musim", loc="center", fontsize=50)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=30)

    st.pyplot(fig)

#This section is average registered users of each month
with tab3:
    st.header("Jumlah pengguna Registered rata-rata per musim")
    fig, ax = plt.subplots(figsize=(65, 35))

    colors = ["#4287f5", "#030bfc", "#42f551", "#d742f5"]

    sns.barplot(x="season", y="registered", data=users_df, palette=colors)
    ax.set_ylabel(None)
    ax.set_xlabel("Musim", fontsize=30)
    ax.set_title("Jumlah pengguna Bike Sharing Registered rata-rata di setiap musim", loc="center", fontsize=50)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=30)

    st.pyplot(fig)

st.subheader('Data Jumlah pengguna Bike Sharing setiap bulannya')
fig, ax = plt.subplots(figsize=(65, 35))

colors = ["#030bfc", "#030bfc", "#030bfc", "#030bfc", "#030bfc", "#fc6203", "#fc6203", "#fc6203", "#fc6203", "#030bfc", "#030bfc", "#030bfc"]

sns.barplot(x="mnth", y="total_users", data=monthly_user_df, palette=colors)
ax.set_ylabel(None)
ax.set_xlabel("Bulan", fontsize=30)
ax.set_title("Jumlah pengguna Bike Sharing rata-rata di setiap bulan Kalender", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader('Data Jumlah pengguna harian Bike Sharing ')
st.line_chart(
   daily_users_df, x="dteday", y="total_users", color="#FF0000"  # Optional
)

