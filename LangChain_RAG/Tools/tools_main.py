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

from tools import tools

load_dotenv()

api_key = os.getenv("MY_DEEPSEEK_API_KEY")
base_url = DEEPSEEK_URL
model = DEEPSEEK_V4_PRO
llm = ChatOpenAI(api_key=api_key, base_url=base_url, model=model)

# 短期记忆
memory = InMemorySaver()

system_prompt = "你是一个AI智能助手，帮助用户解决各种问题"


agent = create_agent(
    model=llm, tools=tools, system_prompt=system_prompt, checkpointer=memory
)


# ----------------------------
# 本地调用测试
response = agent.invoke(
    {"messages": [{"role": "user", "content": "我想用计算器计算？"}]},
    # 配置会话标识，用于区分不同用户
    config={"configurable": {"thread_id": "user_1"}},  # 会话唯一标识，用于区分不同用户
)
print(response)
exit()
