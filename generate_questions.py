import ast
from typing import Final, Any

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

import chatbot
import constants

class GenerateQuestions(chatbot.Chatbot):
    '''Generates queries given a tourist destination.

    Attributes:
      queries: List of queries.
    '''
    
    @property
    def queries(self) -> list[str]:
        return self._queries
        
    def __init__(self):
        super().__init__()        
        self._llm_answer: str = ''
        self._allowed: Final[str] = constants.ALLOWED_CHARS
        self._queries: list[str] = []
        self._prompt_template = open(
            constants.GENERATE_QUESTIONS_PROMPT_FILE
            ).read().replace('{num_queries}', str(constants.NUM_QUERIES))
        
    def _parse_questions(self) -> None:
        if self._llm_answer:
            for input in self._llm_answer:
                temp = ''
                for letter in input:
                    if letter.lower() in self._allowed:
                        temp += letter
                self._queries.append(temp.strip())

    def _llm_chain(self) -> Any:
        prompt = PromptTemplate.from_template(self._prompt_template)
        question_feeder = RunnablePassthrough()        
        return {'question': question_feeder} | prompt | self._chatbot

    def get_questions(self, city: str) -> None:
        '''Generates questions to gather information.

        Args:
          city: Tourist destination to get information for.
        '''
        if not city:
            return []
            
        self._llm_answer = self._llm_chain().invoke(city)
        self._llm_answer = ast.literal_eval(
            getattr(self._llm_answer, 'content', [])
        )
        self._parse_questions()
