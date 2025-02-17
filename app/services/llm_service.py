from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from typing import Dict

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI( model_name ="gpt-4o", temperature=0.7)
        self.summary_parser = JsonOutputParser()

    async def generate_summary(self, document: str) -> str:
        # 定义提示词
        summary_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(
                content="""
                You are a Text Summarization and Matching Assistant. Your task is to analyze user input, extract the core theme, key information, and main points, and generate a concise summary that retains the original meaning. This summary will be used to match articles in a vector database, ensuring the most relevant results are retrieved. Your goal is to provide accurate, concise, and semantically rich summaries to optimize database matching and improve information retrieval efficiency.

                Follow these rules:
                1. Do not include any default or template responses like "I am an AI assistant."
                2. Focus only on summarizing the user's input.
                3. Return the result in the following exact JSON format: {"summary": "Your summary here"}.
            """
            ),
            HumanMessage(content=document)
        ])
        # 创建链
        chain = summary_prompt | self.llm | self.summary_parser
        result = await chain.ainvoke({})

        # 返回解析后的摘要
        return result['summary']

    async def generate_recommendation_reason(
        self,
        query_doc: str,
        retrieved_doc: str
    ) -> str:
        humanSay = f"""
                Explain why these two articles are related and why someone interested in the first document
                might be interested in the second document. Keep it concise and specific.
                
                User's article: {query_doc}
                Related article: {retrieved_doc}
            """

        recommend_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are a helpful assistant that explains document similarities.Summarize it in less than 80 words"),
            HumanMessage(content=humanSay)
        ])
        
        chain = recommend_prompt | self.llm
        result = await chain.ainvoke({})
        return result.content

    async def generate_response(self, prompt: str) -> str:
        messages = [HumanMessage(content=prompt)]
        response = await self.llm.ainvoke(messages)
        return response.content 