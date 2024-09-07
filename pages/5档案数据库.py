import streamlit as st
import pandas as pd
import random
import json

st.logo("./static/logo.png")
st.set_page_config(layout="centered")

@st.cache_resource()
def open_data():    
    with open("./static/output.json", "rb+") as f:
        file = json.load(f)
    return file

file = open_data()
number = len(file)

def search_archive(search_text):
    results = []
    for item in file:
        for value in item.values():
            if isinstance(value, str) and search_text in value:
                results.append(item)
                break  # 找到匹配项后，不需要继续检查其他值
    return results

st.header("档案数据库概况")
col1, col2 = st.columns(2)
col1.metric(label="现有档案数", value=str(number), delta="20", delta_color="inverse")
col2.metric(label="最新档案", value="人民日报1946-2003全文")

st.subheader("最新档案")
df = pd.DataFrame(
    {   
        "archive_id": [random.randint(0, 1000) for _ in range(number)],
        "name": [_["archive"] for _ in file],
        "subject": [_["subject"] if _["subject"] else "无" for _ in file],
        "date": [_["date"][0] if _["date"] else "无" for _ in file],
        "location": [_["location"][0] if _["location"] else "无" for _ in file],
        "signer": [_["signer"] for _ in file],
    }
)
st.dataframe(
    df,
    column_config={
        "name": "档案名",
        "subject": "档案主题",
        "date": "档案时间",
        "location": "档案地点",
        "signer": "档案署名",
    },
    hide_index=True,
    use_container_width=True
)

st.divider()

st.subheader("档案检索")
search_text = st.text_input(label="", placeholder="请输入检索词", key="search_text")

col1, col2 = st.columns(spec=2, gap="large")
with col1:
    search_button = st.button(label="检索档案", key="search_bt", use_container_width=True, type="primary")
with col2:
    clear_button = st.button(label="清空结果", key="clear_bt", use_container_width=True, type="secondary")
    
if search_button:
    with st.spinner("检索中..."):
        result = search_archive(search_text)
    st.subheader("检索结果")
    if result:
        # 创建一个新的DataFrame来显示搜索结果
        result_df = pd.DataFrame(
            {   
                "archive_id": [random.randint(0, 1000) for _ in result],
                "name": [_["archive"] for _ in result],
                "subject": [_["subject"] if _["subject"] else "无" for _ in result],
                "date": [_["date"][0] if _["date"] else "无" for _ in result],
                "location": [_["location"][0] if _["location"] else "无" for _ in result],
                "signer": [_["signer"] for _ in result],
            }
        )
        st.dataframe(
            result_df,
            column_config={
                "name": "档案名",
                "subject": "档案主题",
                "date": "档案时间",
                "location": "档案地点",
                "signer": "档案署名",
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.write("没有找到匹配的档案。")