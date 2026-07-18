from typing import Final

LOCAL_LLM: Final[str] = 'gemma4:e4b'
EMBEDDING_MODEL = 'nomic-embed-text:latest'

TEMPERATURE: Final[float] = 0.7
ALLOWED_CHARS = " -_abcdefghijklmnopqrstuvwxyz'"

# Number of queries to generate.
NUM_QUERIES: Final[int] = 10

# Number of links per query.
NUM_LINKS: Final[int] = 5

# Maximum time (seconds) to query a link.
TIMEOUT = 10

# Minimum number of words per document.
MIN_LENGTH = 100

# Prompt files.
GENERATE_QUESTIONS_PROMPT_FILE: Final[str] = 'prompts/generate_questions_prompt.md'
RAG_PROMPT_FILE: Final[str] = 'prompts/rag_prompt.md'
SUMMARIZER_PROMPT_FILE: Final[str] = 'prompts/summarizer_prompt.md'
HEADINGS_PROMPT_FILE: Final[str] = 'prompts/headings_prompt.md'
