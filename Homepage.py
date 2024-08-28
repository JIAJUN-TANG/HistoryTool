import streamlit as st
import pandas as pd


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

data_df = pd.DataFrame(
    {
        "模型": ["Kimi", "文心一言", "通义千问", "ChatGPT", "Gemini"],
        "是否可用": ["✓", "✓", "开发中", "×", "×"],
        "是否免费": ["否", "是", "开发中", "否", "是"],
        "计算文本Token": ["✓", "✓", "开发中", "×", "×"],
        "计算图像Token": ["✓", "×", "开发中", "×", "×"],
        "文本翻译": ["✓", "✓", "开发中", "×", "×"],
        "图像翻译": ["✓", "×", "开发中", "×", "×"],
    }
)

st.data_editor(
    data_df,
    column_config={
        "widgets": st.column_config.TextColumn(
            "Widgets",
            default="st.",
            max_chars=50,
            validate=r"^st\.[a-z_]+$",
        )
    },
    hide_index=True,
)