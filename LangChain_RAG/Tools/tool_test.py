import os
import sys

_here = os.path.dirname(__file__)
sys.path.insert(0, _here)  # Tools/ — for tools.py
sys.path.insert(0, os.path.dirname(_here))  # project root — for models.py
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from models import DEEPSEEK_URL, DEEPSEEK_V4_PRO
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from datetime import datetime
import webbrowser
from langchain_core.tools import Tool
from langchain.tools import tool

load_dotenv()


@tool
def get_current_time(input: str = "s") -> str:
    """获取当前的时间"""
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    result = f"当前时间{formatted_time}"
    print(result)
    return result


@tool
def open_browser(url, browser_name=None):
    """获取浏览器，打开网站"""
    if browser_name:
        # 获取特定浏览器的控制器
        browser = webbrowser.get(browser_name)
    else:
        # 使用默认浏览器
        browser = webbrowser
    # 打开浏览器并导航到指定的URL
    browser.open(url)


api_key = os.getenv("MY_DEEPSEEK_API_KEY")
base_url = DEEPSEEK_URL
model = DEEPSEEK_V4_PRO
llm = ChatOpenAI(api_key=api_key, base_url=base_url, model=model)

tools = [get_current_time, open_browser]
agent = create_agent(model=llm, tools=tools)

result = agent.invoke({"messages": [{"role": "user", "content": "现在几点了"}]})
print(result)
