import io
import pypdfium2
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from surya.detection import batch_text_detection
import surya.languages
from surya.postprocessing.heatmap import draw_polys_on_image
from surya.schema import TextDetectionResult
from surya.settings import settings
from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
from surya.model.recognition.model import load_model as load_rec_model
from surya.model.recognition.processor import load_processor as load_rec_processor
from pathlib import Path
      

# 定义函数
@st.cache_resource()
def load_det_cached():
    checkpoint = settings.DETECTOR_MODEL_CHECKPOINT
    return load_det_model(checkpoint=checkpoint), load_det_processor(checkpoint=checkpoint)

@st.cache_resource()
def load_rec_cached():
    checkpoint = settings.RECOGNITION_MODEL_CHECKPOINT
    return load_rec_model(checkpoint=checkpoint), load_rec_processor()

def open_pdf(pdf_file):
    stream = io.BytesIO(pdf_file.getvalue())
    return pypdfium2.PdfDocument(stream)

@st.cache_data()
def page_count(pdf_file):
    doc = open_pdf(pdf_file)
    return len(doc)

@st.cache_data()
def get_page_image(pdf_file, page_num, dpi=300):
    doc = open_pdf(pdf_file)
    renderer = doc.render(
        pypdfium2.PdfBitmap.to_pil,
        page_indices=[page_num - 1],
        scale=dpi / 72,
    )
    png = list(renderer)[0]
    png_image = png.convert("RGB")
    return png_image

def text_detection(img) -> (Image.Image, TextDetectionResult):
    pred = batch_text_detection([img], det_model, det_processor)[0]
    polygons = [p.polygon for p in pred.bboxes]
    det_img = draw_polys_on_image(polygons, img.copy())
    return det_img, pred
        
def draw_polygon_and_text(pil_image, text_lines, output_path):
    image = pil_image
    draw = ImageDraw.Draw(image)

    for line in text_lines:
        vertices = line.polygon
        font = ImageFont.truetype("./static/SourceHanSerifCN.otf", size=50)
        
        # 使用 textbbox 计算文本的边界框
        bbox = draw.textbbox((0, 0), line.text, font=font)
        
        # 计算多边形的边界框
        x_coords = [vertex[0] for vertex in vertices]
        y_coords = [vertex[1] for vertex in vertices]
        poly_bbox_left = min(x_coords)
        poly_bbox_top = min(y_coords)
        poly_bbox_right = max(x_coords)
        poly_bbox_bottom = max(y_coords)

        # 确定文本绘制的坐标，使其尽量居中
        text_x = poly_bbox_left + (poly_bbox_right - poly_bbox_left - (bbox[2] - bbox[0])) / 2
        text_y = poly_bbox_top + (poly_bbox_bottom - poly_bbox_top - (bbox[3] - bbox[1])) / 2

        # 在多边形的中心绘制文本
        draw.rectangle([poly_bbox_left, poly_bbox_top, poly_bbox_right, poly_bbox_bottom], fill=(255,255,255))
        draw.text((text_x, text_y), line.text, font=font, fill=(0, 0, 0))

    # 保存图像
    image.save(output_path)


st.logo("./static/logo.png")

# 定义右侧页面布局
st.set_page_config(layout="centered")

# 加载模型
det_model, det_processor = load_det_cached()
rec_model, rec_processor = load_rec_cached()

# 左侧导航栏
st.sidebar.title("历史档案处理")
function_select = st.sidebar.selectbox("请选择需要使用的功能", options=["检测文本", "文本OCR", "阅读顺序分析", "文本检索"], key="function_sl")
if function_select == "文本OCR":
    languages = st.sidebar.selectbox("Languages", sorted(list(surya.languages.CODE_TO_LANGUAGE.values())))
save_select = st.sidebar.checkbox("自动保存结果")
click_button = st.sidebar.button("开始运行", key="click_bt")

# 右侧主界面
in_file = st.file_uploader("请选择需要处理的历史档案文件", type=["pdf", "png", "jpg", "jpeg", "gif", "webp"])
if in_file is None:
    st.stop()
else:
    file_name = in_file.name.split(".")[0]

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
elif function_select == "文本OCR" and click_button:
    langs = [value for key, value in surya.languages.LANGUAGE_TO_CODE.items() if key == languages]
    predictions = run_ocr([pil_image], [langs], det_model, det_processor, rec_model, rec_processor)
    text_lines = " ".join([_.text for _ in predictions[0].text_lines])
    save_path = Path(f"./cached_images/{file_name}/{file_name}_{page_number}_translated.png")
    draw_polygon_and_text(pil_image, predictions[0].text_lines, save_path)
    with col2:
        translated_image = Image.open(save_path).convert("RGB")
        st.image(translated_image, caption="处理后图像", use_column_width=True)
    st.divider()
    st.subheader("OCR文本")
    st.write(text_lines)
with col1:
    image_path = Path(f"./cached_images/{file_name}/{file_name}_{page_number}.png")
    original_image = Image.open(image_path).convert("RGB")
    st.image(original_image, caption="待处理图像", use_column_width=True)
