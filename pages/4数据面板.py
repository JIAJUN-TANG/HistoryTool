import streamlit as st
from Authentic import get_api_key, get_authentication
import pandas as pd
from datetime import datetime
import json

st.logo("./static/logo.png")

balance_dict = {}

file_path = "./static/balance_data.txt"
try:
    with open(file_path, "r") as file:
        balance_dict = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    balance_dict = {}
today = datetime.now().strftime("%Y-%m-%d")
if today not in balance_dict:
    balance_dict[today] = {}
api_key_dict = get_api_key("API_Key.json")
for model, api_key in api_key_dict.items():
    current_balance = get_authentication(model, api_key)
    if current_balance:
        balance_dict[today][model] = current_balance

data_list = []
for date, models in balance_dict.items():
    for model, balance in models.items():
        data_list.append({"日期": date, "模型": model, "余额": balance})

usage_df = pd.DataFrame(data_list, columns=["日期", "模型", "余额"])

st.set_page_config(layout="centered")

st.subheader("余额情况")
col1, col2 = st.columns([.5, .5])
with col1:
    st.dataframe(usage_df)
with col2:
    st.line_chart(usage_df, x="日期", y="余额", color="模型", x_label="日期", y_label="余额", use_container_width=True)

st.divider()