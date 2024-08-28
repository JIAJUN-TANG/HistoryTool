import io
import os
import json
import pypdfium2
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from Authentic import get_api_key, get_authentication
from openai import OpenAI
from pathlib import Path
import requests
import qianfan
from qianfan.resources.tools import tokenizer
import textwrap
import re
# from surya.model.detection.model import load_model, load_processor
# from surya.model.recognition.model import load_model as load_rec_model
# from surya.model.recognition.processor import load_processor as load_rec_processor
# from surya.ocr import run_ocr
# from surya.settings import settings

# 定义函数
# @st.cache_resource()
# def load_det_cached():
#     checkpoint = settings.DETECTOR_MODEL_CHECKPOINT
#     return load_model(checkpoint=checkpoint), load_processor(checkpoint=checkpoint)

# @st.cache_resource()
# def load_rec_cached():
#     return load_rec_model(), load_rec_processor()

# det_model, det_processor = load_det_cached()
# rec_model, rec_processor = load_rec_cached()

# def get_ocr(in_file):
#     images = [Image.open(in_file)]
#     langs = [["en"]]
#     predictions_by_image = run_ocr(images, langs, det_model, det_processor, rec_model, rec_processor)
#     all_text = []
#     for pred in predictions_by_image:
#         text_lines = [line.text for line in pred.text_lines]
#         all_text.append("\n".join(text_lines))
#     return all_text

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
    output_dir = f'./cached_images/{file_name}'
    output_path = os.path.join(output_dir, f"{file_name}_{page_number}.png")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pil_image.save(output_path, "PNG")
    
def get_estimate_token(model, api_key, in_file):
    if model == "Kimi":
        client = OpenAI(
            api_key = api_key,
            base_url = "https://api.moonshot.cn/v1"
        )
        file_object = client.files.create(file = in_file, purpose="file-extract")
        file_content = client.files.content(file_id = file_object.id).text
        headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
        data = {
    "model": "moonshot-v1-128k",
    "messages": [
        {"role" : "system", "content" : "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你是一位历史研究的专家。"},
        {"role": "system", "content": file_content,
    },
        {"role": "user", "content": "请你为我翻译这个图像中的文本，尽可能使结果文本的排版和图像接近，只返回翻译结果。"}
    ]
}
        response = requests.post(
    "https://api.moonshot.cn/v1/tokenizers/estimate-token-count",
        headers=headers,
        data=json.dumps(data)
)
        response_data = response.json()
        total_tokens = response_data.get("data", {}).get("total_tokens")
#     elif model == "文心一言":
#         os.environ["QIANFAN_AK"] = api_key.get("client_id")
#         os.environ["QIANFAN_SK"] = api_key.get("secret_id")
#         text_list=get_ocr(in_file)
#         total_tokens = tokenizer.Tokenizer().count_tokens(
#         text="".join(text_list),
#         mode='remote',
#         model="ernie-speed-128k"
# )  
    return total_tokens
        
def get_chat_completion(model, api_key, in_file, prompt):
    if model == "Kimi":
        client = OpenAI(
            api_key = api_key,
            base_url = "https://api.moonshot.cn/v1"
        )
        file_object = client.files.create(file = in_file, purpose="file-extract")
        file_content = client.files.content(file_id = file_object.id).text
        messages = [
        {"role" : "system", "content" : "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你是一位历史研究的专家。"},
        {"role": "system", "content": file_content,
    },
        {"role": "user", "content": f"{prompt}。判断翻译后的最后一句话是否完整，若完整则Completion为1，不完整则为0。将结果以json格式返回，格式为'Content': '此处为翻译后文本', 'Completion':'此处为判断是否完整参数'"}
    ]
        completion = client.chat.completions.create(
    model = "moonshot-v1-128k",
    messages = messages,
    response_format={"type": "json_object"},
    temperature = 0
    )
        return completion.choices[0].message.content
    # elif model == "文心一言":
    #     os.environ["QIANFAN_AK"] = api_key.get("client_id")
    #     os.environ["QIANFAN_SK"] = api_key.get("secret_id")
    #     content = get_ocr(in_file)
    #     chat_comp = qianfan.ChatCompletion()
    #     resp = chat_comp.do(model="ERNIE-Speed-128K",system = "你是一位精通中英等语言的专家，也是一位历史档案研究者，出了结果不要返回其他任何东西", messages=[{"role": "user",
    #                                                             "content": f"{prompt}。判断翻译后的最后一句话是否完整，若完整则Completion为1，不完整则为0。将结果以json格式返回，格式为'Content': '此处为翻译后文本', 'Completion':'此处为判断是否完整参数'。内容如下: {content}"}],
    #                         temperature = 0.1)
    #     result = re.search(r"\{(.*?)\}", resp["body"]["result"]).group(0)
    #     return result
    
def make_picture(translated_content, file_name, page_number):
    width, height = 568, 876
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    image = Image.new('RGB', (width, height), background_color)
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
    options=["ChatGPT", "Kimi", "Gemini", "文心一言"],
    help="ChatGPT和Gemini模型暂时不可用，使用文心一言时请勿连接VPN"
)

if 'api_key' not in st.session_state:
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

in_file = st.file_uploader("请选择需要处理的历史档案文件")
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
else:
    pil_image = Image.open(in_file).convert("RGB")

@st.experimental_dialog("提醒")
def my_dialog_function():
    save_prompt(prompt_text)
    st.write("当前提示词保存成功！")
prompt_text = st.text_area("提示词，将上传给大模型API", value=default_prompt)
save_prompt_bt = st.button("保存提示词", on_click=my_dialog_function)

if pil_image is None:
    st.stop()

col1, col2 = st.columns([.5, .5])
with col1:
    st.image(pil_image, caption="待处理图像", use_column_width=True)

if calculation_button:
    save_to_file(file_name, pil_image, page_number)
    image_file = Path(f"./cached_images/{file_name}/{file_name}_{page_number}.png")
    estimate_token = get_estimate_token(in_model, in_api_key, image_file)
    token_container = st.info(f"翻译该页面预计需要消耗 {estimate_token} token。")
    
if translation_button:
    save_to_file(file_name, pil_image, page_number)
    image_file = Path(f"./cached_images/{file_name}/{file_name}_{page_number}.png")
    translated_content = get_chat_completion(in_model, in_api_key, image_file, prompt_text)
    translated_content = json.loads(translated_content)
    translated_content = translated_content.get("Content")
    with col2:
        make_picture(translated_content, file_name, page_number)
        translated_image = Path(f"./cached_images/{file_name}/{file_name}_{page_number}_translated.png")
        translated_image = Image.open(translated_image).convert("RGB")
        st.image(translated_image, caption="处理后图像", use_column_width=True)
    st.markdown("---")
    title_t2 = st.subheader("翻译文本")
    display_content = st.markdown(translated_content)