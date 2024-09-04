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
   ### 处理功能支持情况
    - 本地档案处理功能暂未上线。
"""
)

st.markdown(
   """
   ### 翻译功能支持情况
    - Kimi已支持所有功能，其文件上传为上传后OCR；
    - ChatGPT已支持所有功能，官方API请使用VPN，其文件上传为图像理解；
    - 文心一言已支持所有功能，其文件上传为上传后OCR；
    - 通义千文已支持所有功能，其文件上传为上传后OCR，后续将开发图像理解；
    - Gemini暂不支持
"""
)

st.markdown(
   """
   ### 图谱功能支持情况
    - 档案知识图谱自动挖掘功能开发中。
"""
)