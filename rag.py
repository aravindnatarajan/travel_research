from collections.abc import Mapping, Sequence

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter as rcts
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma

import constants
import chatbot

class RAG(chatbot.Chatbot):
    '''Retrieval Augemented Generation module.

    Answers a list of questions provided context.
    Pass in 'documents' which is a list of documents.
    Call answer_questions(questions) where 'questions' is a list of questions.

    Attributes:
      responses: A dictionary mapping question to response.
    '''
    @property
    def responses(self):
        return self._responses
    
    def __init__(
        self,
        documents: Sequence[str],
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
        db_name: str = 'tourist_info',
    ) -> None:
        '''
        Initialize Retrieval Augmented Generation class.

        Args:
            documents: List of documents to use as context.
            chunk_size: Size of chunk, defaults to 1000.
            chunk_overlap: Overlap between chunks, defaults to 100.
            separators: Word separating characters, defaults to white space or period.
            length_function: Function to compute word lengths, defaults to len.
            db_name: Database name, defaults to 'tourist_info'.

        Raised:
            ValueError if the document list is empty.
        '''
        if not documents:
            raise ValueError('Document list cannot be empty.')

        super().__init__()
        self._vector_db = Chroma(
            db_name,
            OllamaEmbeddings(model=constants.EMBEDDING_MODEL)
        )
        self._prompt_template = open(constants.RAG_PROMPT_FILE).read()
        self._text_splitter = rcts(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            length_function=length_function,
        )
        self._documents = documents
        self._responses: Mapping[str, str] = {}
        self._chunks: Sequence[str] = self._chunk_documents()
        self._add_documents()

    def _chunk_documents(self) -> Sequence[str]:
        if not self._documents:
            return []
        return [
            chunk for document in self._documents
            for chunk in self._text_splitter.split_text(document)
        ]
        
    def _add_documents(self) -> None:
        docs = [Document(page_content=chunk) for chunk in self._chunks]
        _ = self._vector_db.add_documents(docs)

    def _chain(self) -> object:
        rag_prompt = PromptTemplate.from_template(self._prompt_template)        
        retriever = self._vector_db.as_retriever()
        question_feeder = RunnablePassthrough()
        return {
            'context': retriever,
            'question': question_feeder
        } | rag_prompt | self._chatbot

    def _answer(self, query: str) -> str:
        answer = self._chain().invoke(query)
        return answer.content
        
    def answer_questions(self, questions: list[str]) -> dict[str, str]:
        '''Answer a list of question using the provided context.

        Args:
          questions: The list of questions to be answered.
        '''
        if questions:
            self._responses = {
                question: self._answer(question)
                for question in questions
            }
