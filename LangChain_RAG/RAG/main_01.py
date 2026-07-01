from models import DEEPSEEK_URL, DEEPSEEK_V4_PRO
import os
from dotenv import load_dotenv

from models import ALI_TEXT_EMBEDDING_V4
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough

"""
 1. 获取文档
 2. 文档切分
 3. 转成向量，存入向量数据库
 4. 检索
 5. 将检索出来的内容 + 问题一起发给llm
 6. LLM生成
"""
load_dotenv()


api_key = os.getenv("MY_DEEPSEEK_API_KEY")
base_url = DEEPSEEK_URL
model = DEEPSEEK_V4_PRO
llm = ChatOpenAI(api_key=api_key, base_url=base_url, model=model)
llm_embedding = DashScopeEmbeddings(
    model=ALI_TEXT_EMBEDDING_V4, dashscope_api_key=os.getenv("ALI_QWEN_API_KEY")
)

# 创建文件加载器,并且读取（基于脚本所在目录拼绝对路径，避免受运行时工作目录影响）
docx_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "人事管理流程.docx"
)
documents = Docx2txtLoader(docx_path).load()
# 文档切分器
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# 切分文档
split_doc = text_splitter.split_documents(documents)


# 将切分好的文档转化成向量 同时存入 Chroma数据库
vector_store = Chroma.from_documents(documents=split_doc, embedding=llm_embedding)
# 检索器
retriever = vector_store.as_retriever()
message = """
 请使用提供的上下文回答下面的问题：
 {question}
 上下文:
 {context}
"""
template = ChatPromptTemplate.from_messages([("human", message)])

chain = {"question": RunnablePassthrough(), "context": retriever} | template | llm

resp = chain.invoke("晋升")
print(resp.content)
