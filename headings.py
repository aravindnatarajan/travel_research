from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

import chatbot
import constants


class Headings(chatbot.Chatbot):
    @property
    def headings_map(self):
        return self._headings_map

    def __init__(self):
        super().__init__()
        self._prompt_template = open(constants.HEADINGS_PROMPT_FILE).read()
        self._headings_map = {}

    def _chain(self):
        prompt = PromptTemplate.from_template(self._prompt_template)
        question_feeder = RunnablePassthrough()
        return {'headings': question_feeder} | prompt | self._chatbot

    def get_headings(self, headings_list: list[str]):
        if headings_list:
            all_text = '\n'.join(headings_list)
            new_headings_text = self._chain().invoke(all_text)
            new_headings_list = new_headings_text.content.split('\n')
            if len(headings_list) == len(new_headings_list):
                self._headings_map = {
                    old: new for old, new in zip(headings_list, new_headings_list)
                    }
