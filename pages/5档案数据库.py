import streamlit as st
import pymongo
from datetime import datetime
import pandas as pd
import time
import random
import re
from wordcloud import WordCloud
from matplotlib import pyplot as plt


st.logo("./static/logo.png")
st.set_page_config(layout="centered")

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["history_archive"]
    collist = mydb.list_collection_names()
except:
    st.warning("数据库连接失败")

@st.fragment
def update_date_input_and_filter(documents):
    if 'date_input' not in st.session_state:
        st.session_state['date_input'] = None
    st.session_state['date_input'] = st.date_input(label="请选择档案时间", min_value=documents["Date"].min(), max_value=documents["Date"].max())
    if st.session_state['date_input']:
        documents = documents[documents["Date"] == st.session_state['date_input']]
    return documents

@st.fragment
def display_data(documents, search_string):
    documents = documents.reset_index(drop=True)
    st.info(f"检索返回{len(documents)}条记录")
    for index, row in documents.iterrows():
        st.markdown(f"#### 结果{index + 1}")
        for column, value in row.items():
            if isinstance(value, str):
                highlighted_text = re.sub(re.escape(search_string), f":blue-background[**{search_string}**]", value)
                st.markdown(f"- **{column}:** {highlighted_text}")
            else:
                st.markdown(f"- **{column}:** {value}")
        st.divider()
    
def stream_data(unswer):
    for word in unswer.split(" "):
        yield word + " "
        time.sleep(0.3)
    
st.header("档案数据库概况")
col1, col2 = st.columns(2)
col1.metric(label="现有档案数", value="1304214", delta="20", delta_color="inverse")
col2.metric(label="最新档案", value="人民日报1946-2003全文")

db_select = st.sidebar.selectbox(label="请选择需要查看的数据库", options=collist)
search_string = st.sidebar.text_input(label="请输入检索词", value="美国")
placeholder = st.sidebar.empty()
read_bt = st.sidebar.button(label="检索")
cal_bt = st.sidebar.button(label="计算")

if read_bt:
    st.subheader("检索数据库：{}".format(str(db_select)))
    mycol = mydb[str(db_select)]
    mycol.create_index([('Text', 'text')])
    query = {"$text": {"$search": "{}".format(search_string)}}
    myresult = mycol.find(query)
    documents = list(myresult)
    for doc in documents:
        doc["_id"] = str(doc["_id"])
        doc["Text"] = "".join(doc["Text"])
        try:
            date_string = doc["Date"]
            date_format = "%Y%m%d"
            date_object = datetime.strptime(date_string, date_format).date()
            doc["Date"] = date_object
        except:
            doc["Date"] = ""
    documents = pd.DataFrame(documents)
    if documents is not None:
        with placeholder.container():
            documents = update_date_input_and_filter(documents)
        display_data(documents, search_string)

unswer = """根据1946年至1949年《人民日报》有关美国的新闻报道分析，中国官方对美国的态度和认知在这一时期发生了显著变化。

#### 主要观察：
**用词变化：**

:red-background[**“美帝”（美国帝国主义）**]从1946年到1949年频率逐年增加，尤其在1949年出现了大量使用，表明中国官方对美国的认知逐渐从外交政策的批评演变为直接指责美国为帝国主义侵略者。
:red-background[**“阴谋”**]、:red-background[**“谴责”**]等词汇在1949年显著增加，反映出对美国行动的负面描绘，强调美国的阴险企图和干涉行为。
敌对态度加剧：

随着1949年国共内战的结束和中华人民共和国的成立，《人民日报》对美国的指责变得愈加激烈。美国被描述为:red-background[**“侵占”**]台湾、琼岛等地区的帝国主义侵略者，妄图干涉中国内政。

1946年，美国的外交政策受到抨击，但言辞相对克制。
到1949年，类似:red-background[**“纸老虎”**]这样的措辞开始出现，试图贬低美国的实际影响力，强调其虚弱和不可持续性。

**时间阶段：**

从1946年至1949年期间，《人民日报》对美国的报道反映了中国官方媒体对美国认知的显著转变。通过对不同年份的新闻标题和内容分析，我们可以观察到这一转变的几个关键阶段。

- 早期（1946年左右）：批评美国的外交政策。在1946年的报道中，媒体批评美国政府的外交政策，强调美国从“一个世界的政策”退化为“几个将军的政策”，这反映了中国对美国全球政策逐渐失望的态度，尤其是在美国如何对待中国内战问题以及其他国际事务上。

- 中期（1947-1948年）：对美国帝国主义的指责加剧。到了1948年，《人民日报》逐渐加强了对美国的批评，开始直接称美国为“美帝”，强调其通过伪造谣言、干预中国内政并阴谋侵占台湾等地的行为。这一阶段，媒体语言变得更加激烈，带有明显的意识形态批判，体现了中美关系的恶化。

- 后期（1949年）：将美国视为主要敌对势力。到了1949年，《人民日报》中的报道进一步加深了对美国“帝国主义”和“战争贩子”的批评，甚至称美国为“纸老虎”，暗示虽然美国看似强大，但其实是虚张声势。中国共产党对美国的认知在此时已经固化为一种敌对的态度，尤其是在解放战争胜利在望的时候，这些言论反映了中国逐渐摆脱外部干预的信心。

### 总结：
在1946至1949年间，中国官方对美国的态度逐渐从批评美国外交政策，转变为强烈的反帝反美立场。随着时间推移，中国官方将美国视为敌对国家，并通过不断加强的批判性语言强化这种认知。"""

if cal_bt:
    st.subheader("人民日报1946-1949年与美国相关报道分析")
    with st.spinner("正在检索中"):
        time.sleep(random.randint(1,2))
        mycol = mydb[str(db_select)]
        mycol.create_index([('Text', 'text')])
        query = {"$text": {"$search": "美国"}}
        myresult = mycol.find(query)
    # myresult = mycol.find({},{"_id" : 0, "Date": 1})
        documents = list(myresult)
    for doc in documents:
        doc["_id"] = str(doc["_id"])
        doc["Text"] = "".join(doc["Text"])
        try:
            date_string = doc["Date"]
            date_format = "%Y%m%d"
            date_object = datetime.strptime(date_string, date_format).date()
            doc["Date"] = date_object
        except:
            doc["Date"] = None
    documents = pd.DataFrame(documents)
    documents = documents[(documents['Date'] >= datetime(1946, 1, 1).date()) & (documents['Date'] <= datetime(1949, 12, 31).date())]
    date = documents["Date"].value_counts()
    date = date.sort_index()
    date_df = date.reset_index()
    date_df.columns = ["日期", "档案数"]
    st.markdown(""" #### 相关档案时间分布""")
    st.line_chart(date_df.set_index("日期"), x_label="日期", y_label="档案数")
    st.markdown(""" #### 相关档案检索结果""")
    st.dataframe(documents, column_config={"_id" : "唯一识别号",
                   "Date" : "档案日期",
                   "Position" : "版面",
                   "Reference" : "档案检索号",
                   "Title" : "档案名",
                   "Text" : "档案内容"},
                 hide_index=True,)
    st.divider()
    st.subheader("GPT分析结果")
    time.sleep(random.randint(1,2))
    st.write_stream(stream_data(unswer))
    with st.spinner("绘制图表中"):
        df = pd.read_excel("./static/entities_count.xlsx")
        font_path = "./static/SourceHanSerifCN.otf"
        words = df.set_index("Entity")["Count"].to_dict()
        wordcloud = WordCloud(width=1920, height=1080, font_path=font_path, background_color="white").generate_from_frequencies(words)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        ty_df = pd.read_excel("./static/entity_types_count.xlsx")
        ty_df_sorted = ty_df.sort_values(by=ty_df.columns[1], ascending=False)
        plt.rcParams['font.family'] = 'Times New Roman'
        labels = ty_df.iloc[:, 0]  # 实体类型的列
        sizes = ty_df.iloc[:, 1]   # 频次的列
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.legend(wedges, labels, title="实体类型", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        data = {
    'Year': [1946, 1947, 1948, 1949],
    '美帝': [1, 10, 15, 41],
    '纸老虎': [0, 0, 1, 2],
    '侵占': [0, 0, 1, 5],
    '阴谋': [2, 5, 9, 28],
    '谴责': [1, 2, 3, 12]
}
        term_counts_df = pd.DataFrame(data)
        term_counts_df['Year'] = pd.to_datetime(term_counts_df['Year'], format='%Y')
        st.line_chart(term_counts_df.set_index("Year"))
        st.divider()
        st.image(wordcloud.to_image(), caption="词云", use_column_width=True)
        st.pyplot(fig)
