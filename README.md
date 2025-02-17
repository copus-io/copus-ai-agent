# Copus 如何接入通过LangChain 接入llm


[LangChain](https://python.langchain.com/docs/get_started/introduction.html)

### 第一步：
从mongodb读取数据，构建向量数据库，向量数据库采用chromadb，使用的chatgpt的embedding模型
### 第二步：
用fastapi构建接口，获取用户的输入信息，然后调用llm去获取输入信息的摘要
### 第三步：
用得到的摘要信息查询向量数据库，获取相似度最高的信息
### 第四步：
将相似度最高的信息交给llm，让它生成推荐理由，然后将理由和对应的作品的uuid返回给用户

