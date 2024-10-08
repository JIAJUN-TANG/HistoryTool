import streamlit as st

st.set_page_config(layout="wide")
st.logo("./static/logo.png")

tab1, tab2, tab3 = st.tabs(["关于我们", "联系方式", "致谢"])

with tab1:
    st.header("南京大学数智文献实验室")
   
    st.subheader("成员单位")
    st.image("./static/logo.png")
    
    st.subheader("项目组成员")
    
    col1, col2, col3 = st.columns(3)
    with col1.container():
        st.image("./static/taowang.png")
        st.markdown('<div style="width: 100%;"><a href="https://history.nju.edu.cn/wt/main.htm">王涛</a>，湖北荆州人，2001年毕业于北京师范大学历史系，获学士学位；2008年毕业于北京大学历史系，获历史学博士学位；曾在德国弗莱堡（Freiburg）大学、慕尼黑大学、美国哈佛大学等高校访问。现为南京大学历史学院教授，主要研究领域为德国史、教会史、数字史学等方向。</div>', unsafe_allow_html=True)
    with col2.container():
        st.image("./static/yangsun.jpg")
        st.markdown('<div style="width: 100%;"><a href="https://history.nju.edu.cn/sy/main.htm">孙杨</a>，生于江苏南京，2009年12月毕业于南京大学历史学系中国近现代史专业，获历史学博士学位。现为南京大学历史学院副教授、香港研究所所长、南京大学-约翰斯·霍普金斯大学中美文化研究中心（HNC）授课教师，担任全国港澳研究会会员、江苏省统一战线理论研究会理事、江苏省中国近现代史学会常务理事。江苏“紫金文化人才培养工程”文化优青培养对象（社科优青）。主要研究领域为20世纪中国政治史、外交史以及香港史。</div>', unsafe_allow_html=True)
    with col3.container():
        st.image("./static/binzhang.jpg")
        st.markdown('<div style="width: 100%;"><a href="https://im.nju.edu.cn/zb/list.htm">张斌</a>，南京大学信息管理学院副教授、博士生导师，管理学博士，中国史博士后。主要研究领域为数据智能与知识工程，数据合规与隐私保护，数字出版与知识服务。</div>', unsafe_allow_html=True)
    st.divider()
        
    
    col4, col5, col6 = st.columns(3)
    with col4.container():
        st.image("./static/qingli.jpg")
        st.markdown('<div style="width: 100%;"><a href="https://history.nju.edu.cn/lq1/main.htm">李庆</a>，男，1985年生，四川射洪人。2009年毕业于中南财经政法大学外国语学院英语系，2011年毕业于浙江大学哲学系外国哲学专业，2016年1月毕业于澳门大学历史系，获历史学博士学位，2018年9月从浙江大学世界史博士后流动站出站，现任南京大学历史学院副教授。先后在《历史研究》《世界历史》《中国经济史研究》等重要学术刊物发表论文十余篇；主持国家社科基金重点项目、国家社科基金青年项目各1项，负责国家社科基金重大项目子课题1项；曾获南京大学青年教师人文科研原创奖（2021）、江苏省哲学社会科学优秀成果奖三等奖（2023）等。</div>', unsafe_allow_html=True)
    with col5.container():
        st.image("./static/renxie.jpg", width=200)
        st.markdown('<div style="width: 100%;"><a href="https://xueheng.nju.edu.cn/yjry/zzry/20240618/i268867.html">谢任</a>，历史学博士，南京大学马克思主义学院助理研究员。攻读博士学位期间，曾以联合培养博士生的身份赴日本京都大学留学一年。主要从事中共党史研究、抗日战争史研究以及学衡派研究。著有《陷都政治：日本在南京的记忆建构与遗迹变迁》（生活·读书·新知三联书店，2023年），在《学海》《党史研究与教学》《读书》和Chinese Studies in History、『非文字資料研究』等中、英、日文学术刊物上发表论文十余篇，主持国家社科基金青年项目、江苏省社科基金文脉专项等科研课题。</div>', unsafe_allow_html=True)
    with col6.container():
        st.markdown('<div style="width: 100%;"><a href="https://history.nju.edu.cn/jbw1/main.htm">金伯文</a>，历史学博士，南京大学历史学院准聘助理教授。</div>', unsafe_allow_html=True)
    st.divider()
        
    col7, col8, col9 = st.columns(3)
    with col7.container():
        st.image("./static/niandayao.jpeg", width=300)
        st.markdown('<div style="width: 100%;"><a href="https://history.nju.edu.cn/ynd1/main.htm">姚念达</a>，南京大学历史学院专职科研岗。武汉大学历史学院历史学学士，北京大学历史系历史学博士。美国哥伦比亚大学访问学者。研究方向为美国对外关系史、冷战史、美国环境外交史</div>', unsafe_allow_html=True)
    with col8.container():
        st.image("./static/jiajuntang.jpg", width=200)
        st.markdown('<div style="width: 100%;"><a href="https://sites.google.com/view/jiajun-tang/homepage">唐嘉骏</a>，南京大学信息管理学院硕士研究生。毕业于中南大学人文学院，获学士学位。研究方向为计算社会科学、数字人文。</div>', unsafe_allow_html=True)

with tab2:
    st.header("联系方式")
    st.markdown("""### 唐嘉骏""")
    st.markdown("""
            1. 邮箱：jiajuntang1101@smail.nju.edu.cn
                
            2. 电话: +86 16680808521
            
            3. 个人主页：https://sites.google.com/view/jiajun-tang/homepage""")