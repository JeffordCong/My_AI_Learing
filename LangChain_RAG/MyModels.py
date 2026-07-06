import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from models import DEEPSEEK_URL, DEEPSEEK_V4_PRO

load_dotenv()

api_key = os.getenv("MY_DEEPSEEK_API_KEY")
base_url = DEEPSEEK_URL
model = DEEPSEEK_V4_PRO
llm = ChatOpenAI(api_key=api_key, base_url=base_url, model=model)
