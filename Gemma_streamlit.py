import streamlit as st
import json
import re
import accelerate

from langchain_community.document_loaders import NotebookLoader
from langchain_core.messages import HumanMessage, SystemMessage
from transformers import AutoTokenizer, AutoModelForCausalLM
#from peft import LoraConfig
#from transformers import BitsAndBytesConfig
import torch
import gc

gc.collect() 
st.title("🦜🔗 Gemma Code Explanation")
torch.cuda.empty_cache()

# Hugging face API Key
with open('ignore.json','r') as f:
    key = json.load(f)
HUGGING_FACE_KEY = key['HUGGING_fACE']
print('key',HUGGING_FACE_KEY)

# config lora



# Model & Tokenizer loading
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it",                                        
                                             device_map="auto")
model.config.use_cache = False
def generate(model, tokenizer, text, token_size=30):
    inputs = tokenizer(text, return_tensors="pt")#.to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=token_size)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

print(HUGGING_FACE_KEY)
def generate_response(model, tokenizer, text):
    st.write("Answer:")
    st.markdown(generate(model, tokenizer, text))

# file upload , 파일 형삭 ipynb
st.title("📝 Code Summary")
uploaded_file = st.file_uploader("Upload an article", type=("ipynb"))

# Notebook 파싱 함수
loader = NotebookLoader(
    uploaded_file
)


# system instruction
#question = "Make blog script with markdown formet  for developer that explains this code. please write code block with the related code too."
question = "Explain this code"
# API key를 넣지 않은 경우
if uploaded_file and question and not HUGGING_FACE_KEY:
    st.info("Please add your OpenAI API key to continue.")


if uploaded_file and question and HUGGING_FACE_KEY:
    # 파일 json parsing
    data = json.load(uploaded_file)
    #print(data.keys())
    
    text_for_article = ''
    article = []
    # source code 부분 파싱
    for idx,_ in enumerate(data['cells']):
        for i, line in enumerate(data['cells'][idx]['source']):
            # 주석 부분 제거
            if '#' not in line:
                
                line = re.sub(r'\s+',' ',line)
                line = line.replace('\n+','\n')
                
                text_for_article += line+'\n'
            if len(text_for_article) > 2000:
                article.append(text_for_article)
                text_for_article = ''

        if len(text_for_article) > 0:
            article.append(text_for_article)
        text_for_article = ''

    # 각 cell에 있는 source code를 나눠서 prompt 구성
    for text_len,code_str in enumerate(article):
        prompt = f"{question} Here's an code:\n\n{code_str}"
        messages = [
            SystemMessage(
                content=f"{question}"
            ),
            HumanMessage(
                content=f"{prompt}."
            ),
        ]

        response = f"{prompt}"
        st.code(code_str)
        st.write(generate_response(model,tokenizer,response))