import streamlit as st
import tempfile
import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import pandas as pd

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from bertopic.vectorizers import ClassTfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

import json

import spacy
nlp = spacy.load('en_core_web_trf')
from spacy.matcher import Matcher
import networkx as nx

st.logo("./static/logo.png")

st.set_page_config(layout="centered")

def parse_epub(in_file):
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, in_file.name)
    with open(path, "wb") as f:
            f.write(in_file.getvalue())
    book = epub.read_epub(path)
    data = []
    pattern = re.compile(r'^\d+\. ')
    date_pattern = re.compile(r'\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}(,|) \d{4}\b')
    location_pattern = re.compile(r'(.*?), (January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}(,|) \d{4}')
      
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.content
            soup = BeautifulSoup(content, 'lxml')

            # 查找所有的h3标签
            h3s = soup.find_all('h3')
            for h3 in h3s:
                h3_text = h3.get_text(separator=" ").replace(" 1  ", "")

                # 检查标题是否以数字加点开头
                if pattern.match(h3_text):
                    # 获取h3下的所有p和li标签文本
                    content_tags = h3.find_all_next(["p", "li"])
                    content_text = [content.get_text().strip(" ") for content in content_tags]
                    
                    signers = h3.find_all_next("span", class_="signed")
                    for signer in signers:
                        raw_text = signer.encode_contents()
                        processed_text = raw_text.replace(b'<br>', b'\n').replace(b'<br/>', b'\n')
                        signer = processed_text.decode('utf-8')
                        signer = signer.split("\n")
                        signer = [_.strip(" ") for _ in signer]

                    foot_tags = h3.find_all_next("div", class_="footnotes")
                    notes = [foot_note.get_text().replace("1\xa0", "") for foot_note in foot_tags]

                    try:
                        date = [re.search(date_pattern, content_text[0]).group(0)]
                    except:
                        date = []
                        
                    try:
                        location = [re.search(location_pattern, content_text[0]).group(1)]
                    except:
                        location = []
                        
                    subject = None

                    for i, item in enumerate(content_text):
                        if "subj" in item.strip().lower() and i+1 < len(content_text):
                            subject = content_text[i+1].strip()
                            break
                        else:
                            subject = []
                            
                    reference = None

                    for i, item in enumerate(content_text):
                        if "ref" in item.strip().lower() and i+1 < len(content_text):
                            reference = content_text[i+1].strip()
                            break
                        else:
                            reference = []
                        
                    # 将信息添加到列表中的字典
                    data.append({
                        "archive" : h3_text,
                        "subject" : subject,
                        "reference" : reference,
                        "date" : date,
                        "location" : location,
                        "content" : content_text,
                        "signer" : signer,
                        "note": notes
                    })

    return data

def english_word_cut(mytext):
    sentence = " ".join(mytext)
    stop_list = []
    try:
        with open("./static/stopwords.txt", encoding='utf-8') as stopword_list:
            stop_list = [line.strip() for line in stopword_list]
    except FileNotFoundError:
        st.warning("停用词表不存在！")
    word_list = []
    words = re.findall(r'\b\w+\b', sentence)   
    for word in words:
        word = word.lower()
        if word in stop_list or len(word) < 2:
            continue        
        word_list.append(word)
    return " ".join(word_list)

def run_bertopic(document):
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    umap_model = UMAP(n_neighbors=15, n_components=2, min_dist=0.0, metric='cosine')
    hdbscan_model = HDBSCAN(min_cluster_size=10, metric='euclidean', prediction_data=True)
    vectorizer_model = CountVectorizer(stop_words="english")
    ctfidf_model = ClassTfidfTransformer()
    topic_model = BERTopic(
    embedding_model=embedding_model,    # Step 1 - Extract embeddings
    umap_model=umap_model,              # Step 2 - Reduce dimensionality
    hdbscan_model=hdbscan_model,        # Step 3 - Cluster reduced embeddings
    vectorizer_model=vectorizer_model,  # Step 4 - Tokenize topics
    ctfidf_model=ctfidf_model,          # Step 5 - Extract topic words
    top_n_words=10,
)
    topic_model.fit(document)
    return topic_model

def display_bertopic(document, topic_model):
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = embedding_model.encode(document, show_progress_bar=False)
    figure = topic_model.visualize_documents(document, embeddings=embeddings)
    figure.write_json("./static/bertopic_results.json")
    filename="./static/bertopic_results.json"
    with open(filename) as f:
        all_data = json.load(f)
        all_data["layout"]["title"]["text"] = ""
    return all_data

in_file = st.file_uploader(label="请选择需要处理的历史档案文件", type=["TXT", "PDF", "EPUB"])

if in_file == None:
    st.stop()

start_bt = st.sidebar.button(label = "开始计算")

if start_bt:
    with st.spinner('档案预处理中...'):
        epub_data = parse_epub(in_file)
        df = pd.DataFrame(epub_data)
        df["content_cutted"] = df.content.apply(english_word_cut)
        filtered_text = df["content_cutted"].tolist()
    with st.spinner('运行Bertopic模型中...'):
        bertopic_model = run_bertopic(filtered_text)
        document_info = bertopic_model.get_document_info(filtered_text)
<<<<<<< HEAD
        topic_info = bertopic_model.get_topic_info()
        topic_info = topic_info[["Topic", "Count", "Name", "Representation"]]
    st.subheader("主题聚类分布")
    st.dataframe(topic_info)
    st.divider()
=======
>>>>>>> d1e40775ac7f335bad446f4c3706eccac7d71e43
    st.subheader("档案主题分布")
    st.dataframe(document_info)
    st.divider()
    with st.spinner('绘制可视化图表中...'):
        display_data = display_bertopic(filtered_text, bertopic_model)
    st.subheader("档案主题聚类可视化")
<<<<<<< HEAD
    st.plotly_chart(display_data)
=======
    st.plotly_chart(display_data)
    st.divider()
    st.subheader("档案知识图谱")
>>>>>>> d1e40775ac7f335bad446f4c3706eccac7d71e43
