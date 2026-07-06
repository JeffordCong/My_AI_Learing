from datetime import datetime
import subprocess, webbrowser
from langchain_core.tools import Tool
from langchain.tools import tool


@tool
def get_current_time(input: str = "s") -> str:
    """获取当前的时间"""
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    result = f"当前时间{formatted_time}"
    print(result)
    return result


def recom_drink(input: str = "") -> str:
    """推荐附近的饮品店"""
    result = """距离您500米内有如下饮料店：\n
    1、蜜雪冰城\n
    2、茶颜悦色\n
    另外距离您200米内有惠民便利店，里面应该有矿泉水或其他饮品"""
    return result


def open_calc(input: str = "") -> str:
    """打开计算器"""
    try:
        subprocess.Popen(["calc.exe"])
        return "计算器已打开"
    except Exception as e:
        return f"打开计算器失败: {str(e)}"


def open_browser(url: str) -> str:
    """打开浏览器访问网址"""
    try:
        webbrowser.open(url=url)
        return f"已经打开浏览器,访问{url}"
    except Exception as e:
        return f"打开浏览器失败: {str(e)}"


tools = [
    Tool(
        name="get_current_time",
        func=get_current_time,
        description="当你想知道现在的时间时调用",
    ),
    Tool(
        name="recom_drink", func=recom_drink, description="用户口渴，推荐附件的饮料店"
    ),
    Tool(name="open_calc", func=open_calc, description="打开计算器"),
    Tool(
        name="open_browser",
        func=lambda url: open_browser(url),
        description="打开本地计算器上的网页浏览器，并接受网站的url作为参数",
    ),
]
