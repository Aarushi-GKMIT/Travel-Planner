import langchain
from langchain_core.globals import set_debug
from langchain_openai import ChatOpenAI

set_debug(True)

class LLMProvider:
    @staticmethod
    def get_llm():
        return ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
        )
