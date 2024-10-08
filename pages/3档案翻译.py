import io
import os
import json
import tempfile
import pypdfium2
import ebooklib
from ebooklib import epub
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from Authentic import get_api_key, get_authentication
from openai import OpenAI
import dashscope
from pathlib import Path
import requests
import qianfan
<<<<<<< HEAD
import textwrap
from bs4 import BeautifulSoup
import base64
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

# 加载模型
det_model, det_processor = load_det_cached()
rec_model, rec_processor = load_rec_cached()
=======
from qianfan.resources.tools import tokenizer
import textwrap
from bs4 import BeautifulSoup
import re
import base64

>>>>>>> d1e40775ac7f335bad446f4c3706eccac7d71e43

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

def save_to_file(file_name, pil_image, page_number):
    output_dir = f"./cached_images/{file_name}"
    output_path = os.path.join(output_dir, f"{file_name}_{page_number}.png")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pil_image.save(output_path, "PNG")
<<<<<<< HEAD
    return output_path
=======
>>>>>>> d1e40775ac7f335bad446f4c3706eccac7d71e43

def get_estimate_token_text(model, api_key, in_file):
    if model == "Kimi":
        headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
        data = {
    "model": "moonshot-v1-128k",
    "messages": [
        {"role" : "system", "content" : "你是一位历史研究的专家。"},
        {"role": "system", "content": in_file,
    },
        {"role": "user", "content": "请你为我翻译这个图像中的文本，只返回翻译结果。"}
    ]
}
        response = requests.post(
    "https://api.moonshot.cn/v1/tokenizers/estimate-token-count",
        headers=headers,
        data=json.dumps(data)
)
        response_data = response.json()
        total_tokens = response_data.get("data", {}).get("total_tokens")
        return total_tokens
    else:
        total_tokens = 0
        return total_tokens

def get_estimate_token(model, api_key, in_file):
    if model == "Kimi":
        client = OpenAI(
            api_key = api_key,
            base_url = "https://api.moonshot.cn/v1"
        )
        headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
        file_object = client.files.create(file = in_file, purpose="file-extract")
        file_content = client.files.content(file_id = file_object.id).text
        data = {
    "model": "moonshot-v1-128k",
    "messages": [
        {"role" : "system", "content" : "你是一位历史研究的专家。"},
        {"role": "system", "content": file_content,
    },
        {"role": "user", "content": "请你为我翻译这个图像中的文本，只返回翻译结果。"}
    ]
}
        response = requests.post(
    "https://api.moonshot.cn/v1/tokenizers/estimate-token-count",
        headers=headers,
        data=json.dumps(data)
)
        response_data = response.json()
        total_tokens = response_data.get("data", {}).get("total_tokens")
        return total_tokens
    else:
        total_tokens = 0
        return total_tokens

def get_chat_completion_text(model, api_key, in_file, prompt):
    if model == "Kimi":
        client = OpenAI(
            api_key = api_key,
            base_url = "https://api.moonshot.cn/v1"
        )
        messages = [
        {"role" : "system", "content" : "你是一位历史研究的专家。"},
        {"role": "system", "content": in_file,
    },
        {"role": "user", "content": prompt}
    ]
        completion = client.chat.completions.create(
    model = "moonshot-v1-128k",
    messages = messages,
    response_format={"type": "json_object"},
    temperature = 0
    )
        return completion.choices[0].message.content
    elif model == "文心一言":
        os.environ["QIANFAN_AK"] = api_key.get("client_id")
        os.environ["QIANFAN_SK"] = api_key.get("secret_id")
        chat_comp = qianfan.ChatCompletion()
        response = chat_comp.do(model="ERNIE-Speed-128K",system = "你是一位擅长多语言的专家，除了结果不要返回其他任何东西", messages=[{"role": "user",
                                                                "content": prompt + in_file}],
                            temperature = 0.1)
        return response["body"]["result"]
    elif model == "ChatGPT-转发":
        client = OpenAI(
    api_key=api_key,
    base_url="https://api.chatanywhere.com.cn/v1"
)
        completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role" : "system", "content" : "你是一位历史研究的专家，精通多种语言。"},
        {"role": "system", "content": in_file,
    },
        {"role": "user", "content": prompt}
        
    ],
    response_format={"type": "json_object"},
    temperature = 0
)   
        return completion.choices[0].message.content
    elif model == "通义千问":
        dashscope.api_key= api_key
        messages = [{"role": "system", "content": "你是一位擅长多语言的专家，也是一位历史档案研究者，除了结果不要返回其他任何东西"},
                    {"role": "system", "content": in_file},
                    {"role": "user", "content": prompt}]
        response = dashscope.Generation.call(model="qwen-max-longtext",
                               messages=messages,
                               temperature=0.1,
                               top_p=0.8,
                               top_k=50,
                               result_format="text",
                               enable_search=True)
        if response.status_code == 200:
            return response
    
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
    
def get_chat_completion(model, api_key, in_file, prompt):
    file_content = encode_image(in_file)
    client = OpenAI(
            api_key = "sk-F2nfwVa0n6KKg1yFNS2e1kxPg8Z8IE7gGMQjd2JnE5CrKMEz",
            base_url = "https://api.moonshot.cn/v1"
        )
    file_object = client.files.create(file=in_file, purpose="file-extract")
    text_content = client.files.content(file_id=file_object.id).text
    if model == "Kimi":
        client = OpenAI(
            api_key = api_key,
            base_url = "https://api.moonshot.cn/v1"
        )
        messages = [
        {"role" : "system", "content" : "你是一位历史研究的专家，精通多种语言。除了翻译结果外请勿添加任何其他内容。"},
        {"role": "system", "content": text_content,
    },
        {"role": "user", "content": f"{prompt}。"}
    ]
        completion = client.chat.completions.create(
    model = "moonshot-v1-128k",
    messages = messages,
    response_format={"type": "json_object"},
    temperature = 0
    )
        return completion.choices[0].message.content
    elif model == "ChatGPT-转发":
        headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}
        payload = {
  "model": "gpt-4o",
  "messages": [
      {
      "role": "system",
      "content": "你是一位历史研究的专家，精通多种语言，因此你很熟悉档案翻译。"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": f"{prompt}。除了翻译结果外请勿添加任何其他内容。"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{file_content}"
          }
        }
      ]
    }
  ],
  "top_p": 1,
  "temperature": 0.1,
  "frequency_penalty": 0,
  "presence_penalty": 0
}
        response = requests.post("https://api.chatanywhere.tech/v1/chat/completions", headers=headers, json=payload)
        response = response.json()["choices"][0]["message"]["content"]
        return response
    elif model == "ChatGPT-官方":
        headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}
        payload = {
  "model": "gpt-4o",
  "messages": [
      {
      "role": "system",
      "content": "你是一位历史研究的专家，精通多种语言，因此你很熟悉档案翻译。"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": f"{prompt}。除了翻译结果外请勿添加任何其他内容。"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{file_content}"
          }
        }
      ]
    }
  ],
  "top_p": 1,
  "temperature": 0,
  "frequency_penalty": 0,
  "presence_penalty": 0
}
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response = response.json()["choices"][0]["message"]["content"]
        return response
    elif model == "文心一言":
        os.environ["QIANFAN_AK"] = api_key.get("client_id")
        os.environ["QIANFAN_SK"] = api_key.get("secret_id")
        chat_comp = qianfan.ChatCompletion()
        response = chat_comp.do(model="ERNIE-Speed-128K",system = "你是一位擅长多语言的专家，除了结果不要返回其他任何东西", messages=[{"role": "user",
                                                                "content": f"{prompt}：{text_content}"}],
                                truncate_overlong_msgs = True,
                                temperature = 0.1)
        response = response["body"]["result"]
        return response
    elif model == "通义千问":
        dashscope.api_key= api_key
        messages = [{"role": "system", "content": "你是一位擅长多语言的专家，除了结果不要返回其他任何东西"},
                    {"role": "system", "content": f"{prompt}。"},
                    {"role": "user", "content": text_content}]
        response = dashscope.Generation.call(model="qwen-max-longcontext",
                               messages=messages,
                               temperature=0.1,
                               top_p=0.8,
                               top_k=50,
                               result_format="text",
                               enable_search=True)
        return response.output.text
    
<<<<<<< HEAD
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
=======
def make_picture(translated_content, file_name, page_number):
    width, height = 568, 876
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)
    font_path = "./static/SourceHanSerifCN.otf"
    font_size = 18
    font = ImageFont.truetype(font_path, font_size)
    text = translated_content
    lines = textwrap.wrap(text, width=width//font_size)
    x = 0
    y = 20
    for line in lines:
        left, top, right, bottom = font.getbbox(line)
        text_height = bottom - top
        draw.text((x, y), line, font=font, fill=text_color)
        y = y + text_height + 10
    image.save(f"./cached_images/{file_name}/{file_name}_{page_number}_translated.png")
>>>>>>> d1e40775ac7f335bad446f4c3706eccac7d71e43

def chapter_to_markdown(chapter):
    soup = BeautifulSoup(chapter.get_body_content(), "html.parser")
    h1_tags = soup.find_all("h1")
    h1_text = "\n".join([f"# {tag.get_text()}" for tag in h1_tags])
    p_tags = soup.find_all("p")
    p_text = "\n".join([f"{tag.get_text()}" for tag in p_tags])
    return f"{h1_text}\n{p_text}"

def save_prompt(new_prompt):
    new_prompt_str = str(new_prompt)
    file_path = "./static/prompts.txt"
    try:
        with open(file_path, "r+", encoding="utf-8") as file:
            prompts = json.load(file)
            if not isinstance(prompts, dict):
                prompts = {}
    except (FileNotFoundError, json.JSONDecodeError):
        prompts = {}

    max_key = max(prompts.keys(), default=-1, key=int)
    max_key = int(max_key)
    next_key = str(max_key + 1)  # 确保key是字符串
    prompts[next_key] = new_prompt_str
    
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(prompts, file, ensure_ascii=False)

  
with open("./static/prompts.txt", "r", encoding="utf-8") as f:
    prompts = f.read()
    prompts = json.loads(prompts)
    default_prompt = prompts.get("0")

# 左侧导航栏
api_key_dict = get_api_key("API_Key.json")
def update_api_key(model):
    default_api_key = api_key_dict.get(model, "")
    st.session_state.api_key = default_api_key
    st.sidebar.text_input("请输入模型的API_Key", value=default_api_key, key="api_key_input")

st.sidebar.title("历史档案翻译")
in_model = st.sidebar.selectbox(
    "请选择需要使用的模型",
    options=["Kimi", "ChatGPT-转发", "ChatGPT-官方", "Gemini", "文心一言", "通义千问"],
    help="ChatGPT-官方需要使用VPN加速，请选择支持地区"
)

if "api_key" not in st.session_state:
    st.session_state.api_key = api_key_dict.get(in_model, "")
update_api_key(in_model)
in_api_key = st.session_state.api_key
api_status = get_authentication(in_model, in_api_key)

if api_status:
    st.sidebar.success(f"当前帐户API可用")
else:
    st.sidebar.error("当前API不可用")
    
calculation_button = st.sidebar.button("计算费用")
translation_button = st.sidebar.button("开始翻译")

# 右侧主界面
st.logo("./static/logo.png")

in_file = st.file_uploader("请选择需要处理的历史档案文件", type=["pdf", "png", "png", "epub", "jpg"])
if in_file is None:
    st.stop()
else:
    file_name = in_file.name.split(".")[0]

filetype = in_file.type
whole_image = False
if "pdf" in filetype:
    page_count = page_count(in_file)
    page_number = st.number_input(f"选择或输入PDF页码，最大为{page_count}：", min_value=1, value=1, max_value=page_count)
    pil_image = get_page_image(in_file, page_number)
elif "epub" in filetype:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, in_file.name)
    with open(path, "wb") as f:
            f.write(in_file.getvalue())
    book = epub.read_epub(path)
    page_count = 0
    epub_content = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            page_count += 1
            epub_content.append(item)
    page_number = st.number_input(f"选择或输入EPUB页码，最大为{page_count}：", min_value=1, value=1, max_value=page_count)
    texts = chapter_to_markdown(epub_content[page_number])
    pil_image = 0
else:
    pil_image = Image.open(in_file).convert("RGB")
    page_number = 1

@st.experimental_dialog("提醒")
def my_dialog_function():
    save_prompt(prompt_text)
    st.write("当前提示词保存成功！")
prompt_text = st.text_area("提示词，将上传给大模型API", value=default_prompt)
save_prompt_bt = st.button("保存提示词", on_click=my_dialog_function)

if pil_image is None:
    st.stop()

col1, col2 = st.columns([.5, .5])
<<<<<<< HEAD
col3, col4 = st.columns([.5, .5])

=======
>>>>>>> d1e40775ac7f335bad446f4c3706eccac7d71e43
with col1:
    if "epub" in filetype:
        st.markdown(texts)
    else:
        st.image(pil_image, caption="待处理图像", use_column_width=True)

if calculation_button:
    if pil_image == 0:
        estimate_token = get_estimate_token(in_model, in_api_key, texts)
    else:
        save_to_file(file_name, pil_image, page_number)
        image_file = Path(f"./cached_images/{file_name}/{file_name}_{page_number}.png")
        estimate_token = get_estimate_token(in_model, in_api_key, image_file)
    token_container = st.info(f"翻译该页面预计需要消耗 {estimate_token} token。")
    
if translation_button:
    if pil_image == 0:
        translated_content = get_chat_completion_text(in_model, in_api_key, texts, prompt_text)
        with col2:
            display_content = st.markdown(translated_content)
    else:
<<<<<<< HEAD
        image_file = Path(save_to_file(file_name, pil_image, page_number))
        translated_content = get_chat_completion(in_model, in_api_key, image_file, prompt_text)
        with col2:
            with st.spinner("正在翻译中..."):
                langs = ["en"]
                # langs = [value for key, value in surya.languages.LANGUAGE_TO_CODE.items() if key == languages]
                predictions = run_ocr([pil_image], [langs], det_model, det_processor, rec_model, rec_processor)
                text_lines = " ".join([_.text for _ in predictions[0].text_lines])
                translated_image = Path(f"./cached_images/{file_name}/{file_name}_{page_number}_translated.png")
                draw_polygon_and_text(pil_image, predictions[0].text_lines, translated_image)
                translated_image = Image.open(translated_image).convert("RGB")
            st.image(translated_image, caption="处理后图像", use_column_width=True)
        with col3:
            title_t1 = st.subheader("原文文本")
            display_content = st.markdown(text_lines)
        with col4:
            title_t2 = st.subheader("翻译文本")
            display_content = st.markdown(translated_content)
=======
        save_to_file(file_name, pil_image, page_number)
        image_file = Path(f"./cached_images/{file_name}/{file_name}_{page_number}.png")
        translated_content = get_chat_completion(in_model, in_api_key, image_file, prompt_text)
        with col2:
            with st.spinner("正在翻译中..."):
                make_picture(translated_content, file_name, page_number)
                translated_image = Path(f"./cached_images/{file_name}/{file_name}_{page_number}_translated.png")
                translated_image = Image.open(translated_image).convert("RGB")
            st.image(translated_image, caption="处理后图像", use_column_width=True)
        st.markdown("---")
        title_t2 = st.subheader("翻译文本")
        display_content = st.markdown(translated_content)
>>>>>>> d1e40775ac7f335bad446f4c3706eccac7d71e43
