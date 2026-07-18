from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

import chatbot
import constants


class Summarizer(chatbot.Chatbot):
    def __init__(self):
        super().__init__()
        self._prompt_template = open(constants.SUMMARIZER_PROMPT_FILE).read()

    def _chain(self):
        prompt = PromptTemplate.from_template(self._prompt_template)
        question_feeder = RunnablePassthrough()
        return {'text': question_feeder} | prompt | self._chatbot

    def summarize(self, documents: list[str]):
        if not documents:
            return ''
        all_text = '\n'.join(documents[::5])
        return self._chain().invoke(all_text)
