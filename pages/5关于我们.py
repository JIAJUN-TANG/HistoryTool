import streamlit as st

st.logo("./static/logo.png")

tab1, tab2, tab3 = st.tabs(["关于我们", "联系方式", "致谢"])

with tab1:
    st.header("南京大学历史档案管理系统开发团队")
   
    col1, col2 = st.columns([.5, .5], gap = "large")
    with col1:
        st.subheader("成员单位")
        st.image("./static/logo.png")
    with col2:
        st.subheader("指导教师")
        st.markdown('<div style="width: 100%;">张斌，南京大学信息管理学院副教授。</div>', unsafe_allow_html=True)
        st.markdown('<div style="width: 100%;">李庆，南京大学历史学院副教授。</div>', unsafe_allow_html=True)
        st.markdown('<div style="width: 100%;">金伯文，南京大学历史学院助理教授。</div>', unsafe_allow_html=True)
        st.markdown('<div style="width: 100%;">姚念达，南京大学历史学院专职科研岗。</div>', unsafe_allow_html=True)
        st.divider()
        st.subheader("主要成员")
        st.markdown('<div style="width: 100%;">唐嘉骏，南京大学信息管理学院2023级硕士研究生。研究方向为计算社会科学、数字人文。</div>', unsafe_allow_html=True)

with tab2:
    st.header("联系方式")
    st.markdown("""### 唐嘉骏""")
    st.markdown("""
            1. 邮箱：jiajuntang1101@smail.nju.edu.cn
                
            2. 电话: +86 16680808521
            
            3. 个人主页：https://sites.google.com/view/jiajun-tang/homepage""")