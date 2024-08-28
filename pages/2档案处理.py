import io
import pypdfium2
import streamlit as st
from PIL import Image
# from surya.detection import batch_text_detection
# import surya.languages
# from surya.model.detection.model import load_model, load_processor
# from surya.schema import TextDetectionResult
# from surya.postprocessing.heatmap import draw_polys_on_image
# from surya.settings import settings

# 定义函数
# @st.cache_resource()
# def load_det_cached():
#     checkpoint = settings.DETECTOR_MODEL_CHECKPOINT
#     return load_model(checkpoint=checkpoint), load_processor(checkpoint=checkpoint)

# def open_pdf(pdf_file):
#     stream = io.BytesIO(pdf_file.getvalue())
#     return pypdfium2.PdfDocument(stream)

# @st.cache_data()
# def page_count(pdf_file):
#     doc = open_pdf(pdf_file)
#     return len(doc)

# @st.cache_data()
# def get_page_image(pdf_file, page_num, dpi=300):
#     doc = open_pdf(pdf_file)
#     renderer = doc.render(
#         pypdfium2.PdfBitmap.to_pil,
#         page_indices=[page_num - 1],
#         scale=dpi / 72,
#     )
#     png = list(renderer)[0]
#     png_image = png.convert("RGB")
#     return png_image

# def text_detection(img) -> (Image.Image, TextDetectionResult):
#     pred = batch_text_detection([img], det_model, det_processor)[0]
#     polygons = [p.polygon for p in pred.bboxes]
#     det_img = draw_polys_on_image(polygons, img.copy())
#     return det_img, pred

st.logo("./static/logo.png")

# 定义右侧页面布局
st.set_page_config(layout="centered")

# 加载模型
# det_model, det_processor = load_det_cached()

# 左侧导航栏
st.sidebar.title("历史档案处理")
function_select = st.sidebar.selectbox("请选择需要使用的功能", options=["检测文本", "文本OCR", "阅读顺序分析", "文本检索"], key="function_sl", disabled=True)
if function_select == "文本OCR":
    languages = st.sidebar.multiselect("Languages", sorted(list(surya.languages.CODE_TO_LANGUAGE.values())), default=["English"], max_selections=4)
save_select = st.sidebar.checkbox("自动保存结果")
click_button = st.sidebar.button("开始运行", key="click_bt")

# 右侧主界面
in_file = st.file_uploader("请选择需要处理的历史档案文件", type=["pdf", "png", "jpg", "jpeg", "gif", "webp"], disabled=True)
if in_file is None:
    st.stop()

filetype = in_file.type
whole_image = False
if "pdf" in filetype:
    page_count = page_count(in_file)
    page_number = st.sidebar.number_input(f"选择或输入PDF页码，最大为{page_count}：", min_value=1, value=1, max_value=page_count)
    pil_image = get_page_image(in_file, page_number)
else:
    pil_image = Image.open(in_file).convert("RGB")
    
if pil_image is None:
    st.stop()

col1, col2 = st.columns([.5, .5])
if function_select == "检测文本" and click_button:
    det_img, pred = text_detection(pil_image)
    with col2:
        st.image(det_img, caption="处理后图像", use_column_width=True)
        
with col1:
    st.image(pil_image, caption="待处理图像", use_column_width=True)