import streamlit as st
import json
import re

from langchain_community.document_loaders import NotebookLoader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from transformer import AutoTokenizer, AutoModelForCausalLM

st.title("🦜🔗 Langchain Quickstart App")


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
# model_name = "gpt-4-0125-preview"
print(openai_api_key)
def generate_response(message):
    llm = ChatOpenAI(model_name = "gpt-4-0125-preview",temperature=0.5, openai_api_key=openai_api_key)
    st.write("Answer:")
    st.markdown(llm.invoke(message).content)

# file upload , 파일 형삭 ipynb
st.title("📝 Code Summary")
uploaded_file = st.file_uploader("Upload an article", type=("ipynb"))
#print(json.load(uploaded_file).keys())
#print(json.load(uploaded_file))
#print(''.join(data['cells'][:]['source']).strip())

# Notebook 파싱 함수
loader = NotebookLoader(
    uploaded_file
)


# system instruction
#question = "Make blog script with markdown formet  for developer that explains this code. please write code block with the related code too."
question = """I am a programmar and you are an expert in datascience.  You have helped many people before me to understand and execute code for various purposes. I will provide lines of Python preceded by three arrow brackets (>>>). You will print out the output formatted in a code block. You should explanations with title on the different results you generate. Provide easy to understand and detailed explanations for beginners. Write your code in English with proper syntax. My first line of Python code is this: [[>>> from functools important reduce; fibonacci = lambda n: reduce(lambda x, _: x+{{x{{-1}}+x{{-2}}}}, range(n-2), {{0, 1}}); print(fibonacci(10))]].And before you start explaination, Make existed header tag link on the top like this link."""

# API key를 넣지 않은 경우
if uploaded_file and question and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")


if uploaded_file and question and openai_api_key:
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
        st.write(generate_response(messages))