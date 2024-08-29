import streamlit as st


st.set_page_config(
    page_title="南京大学历史档案处理工具"
)

st.logo("./static/logo.png")

col1, col2, col3 = st.columns(3)

with col2:
   st.image("./static/logo.png")

st.markdown("""
         ## 欢迎使用南京大学历史档案处理工具"""
         )

st.sidebar.success("请选择您需要使用的功能")

st.markdown(
    """
    南京大学历史档案处理工具是一个基于生成式AI的历史档案信息处理工具。
    
    支持各类历史档案文件（PDF、JPG、PNG等格式）的处理和翻译。通过系统的提示词优化达成最佳效果。
""")

st.markdown(
   """
    - Kimi已支持所有功能
    - ChatGPT已支持所有功能
    - 文心一言暂时只支持EPUB格式翻译
    - 通义千文正在开发中
    - Gemini暂不支持
"""
)