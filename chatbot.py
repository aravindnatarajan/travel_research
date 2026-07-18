from langchain_ollama import ChatOllama

import constants

class Chatbot:
    def __init__(
        self,
        local_llm: str = constants.LOCAL_LLM,
        temperature: float = constants.TEMPERATURE,
    ):
        self._chatbot = ChatOllama(
            model=local_llm,
            temperature=temperature
            )
