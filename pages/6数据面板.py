import streamlit as st
<<<<<<< HEAD
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random
=======
from Authentic import get_api_key, get_authentication
import pandas as pd
from datetime import datetime
import json
>>>>>>> d1e40775ac7f335bad446f4c3706eccac7d71e43

st.logo("./static/logo.png")

balance_dict = {}

file_path = "./static/balance_data.txt"
try:
    with open(file_path, "r") as file:
        balance_dict = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    balance_dict = {}
<<<<<<< HEAD

today = datetime.now().strftime("%Y-%m-%d")
if today not in balance_dict:
    balance_dict[today] = {}

current_balance = random.uniform(0,100)

one_month_ago = datetime.now() - timedelta(days=7)
data_list = []
for model in ["ChatGPT-转发", "ChatGPT-官方", "Kimi", "文心一言"]:
    for date in pd.date_range(end=today, start=one_month_ago).strftime('%Y-%m-%d')[::-1]:
        balance = random.uniform(0, 100)
        data_list.append({"日期": date, "模型": model, "余额": balance})

# 将数据转换为DataFrame
usage_df = pd.DataFrame(data_list)

st.set_page_config(layout="wide")

st.header("数据面板")
st.subheader("近7天用量")
st.line_chart(usage_df, x="日期", y="余额", color="模型", x_label="日期", y_label="余额", use_container_width=True)
st.divider()

st.subheader("访问地址统计")
df = pd.DataFrame(
    np.random.randn(100, 2) / [5, 5] + [32.0603, 118.7969],
    columns=["lat", "lon"],
)
st.map(df)
=======
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

st.header("数据面板")
st.subheader("余额情况")
col1, col2 = st.columns([.5, .5])
with col1:
    st.dataframe(usage_df)
with col2:
    st.line_chart(usage_df, x="日期", y="余额", color="模型", x_label="日期", y_label="余额", use_container_width=True)

st.divider()
>>>>>>> d1e40775ac7f335bad446f4c3706eccac7d71e43
