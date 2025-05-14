import streamlit as st
import pandas as pd

st.title("ダッシュボード")
st.write("カスタマサポートのデータを可視化するダッシュボードです。")

# データの読み込み
@st.cache_data
def load_data():
    # CSVファイルを読み込む
    df = pd.read_csv("data.csv")
    return df
df = load_data()

# データの表示
st.write("データの表示")
st.dataframe(df)