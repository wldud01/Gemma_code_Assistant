import streamlit as st
import json
from langchain.llms import OpenAI

with open('ignore.json','r') as f:
    api_key = json.load(f)
    #print(api_key['api_key'])

openai_api_Key = api_key['api_key']

st.title("🦜🔗 Langchain Quickstart App")
 
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    st.info(llm(input_text))



st.title("📝 File Q&A with Anthropic")
uploaded_file = st.file_uploader("Upload an article", type=("ipynb"))



with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(text)
