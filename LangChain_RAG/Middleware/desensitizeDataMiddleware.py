from langchain.agents.middleware import AgentMiddleware
from langchain.agents import create_agent
from typing import Any, Dict
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from MyModels import llm


class DesensitizeDataMiddleware(AgentMiddleware):

    def __init__(self, patterns: list | None = None):
        super().__init__()
        self.patterns = patterns or [
            (r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[EMAIL]"),
            (r"(\+86)?1[3-9]\d{9}", "[PHONE]"),
        ]

    def desensitize_text(self, text: str) -> str:
        print(f"脱敏前----->>：{text}")
        original_text = text
        for pattern, replacement in self.patterns:
            text = re.sub(pattern, replacement, text)
        if original_text != text:
            print(f"脱敏后: {text}")
        return text

    def before_model(
        self, state: Dict[str, Any], runtime: Any = None
    ) -> Dict[str, Any] | None:
        _ = runtime
        if "messages" not in state:
            return None

        messages = state["messages"]
        processed_any = False

        for message in messages:
            if not (hasattr(message, "content") and isinstance(message.content, str)):
                continue
            content = message.content
            if not content:
                continue
            # 快速预检：含邮箱或手机号特征才处理
            if not ("@" in content or re.search(r"1[3-9]\d{9}", content)):
                continue
            if not processed_any:
                print(".........脱敏中............")
            message.content = self.desensitize_text(content)
            processed_any = True

        if processed_any:
            print("........... 脱敏完成 ........")
            return {"messages": messages}
        return None


if __name__ == "__main__":
    system_prompt = "你是一个专业的论文查询助手，使用arxiv工具为用户查询论文信息，回答需简洁准确，包含论文标题、作者、发表时间和核心摘要。"
    middleware = DesensitizeDataMiddleware()
    agent = create_agent(
        model=llm, system_prompt=system_prompt, middleware=[middleware]
    )

    email_input = (
        "我的邮箱是test.user@example.com，手机号：13112315666，请帮我查询论文1605.08386"
    )
    result = agent.invoke(
        {"messages": [{"role": "user", "content": email_input}]},
        config={"configurable": {"thread_id": "middleware_test_1"}},
    )
    print("结果:", result["messages"][-1].content)
