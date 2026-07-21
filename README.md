# 🌍 Travel Researcher

An automated research agent that takes a target destination, performs deep web research using web scraping and a Retrieval-Augmented Generation (RAG) pipeline, and compiles a comprehensive travel report—powered by local LLMs via **Ollama** or cloud API providers.

---

## 📌 Overview

Planning trips often requires wading through dozens of blogs, forums, and guidebooks to find actionable details on local culture, safety, top sights, food, and logistics. 

**Travel Researcher** automates this end-to-end research workflow:
1. **Query Generation:** Formulates targeted sub-queries covering key dimensions of the destination (attractions, dining, transport, safety, local tips).
2. **Web Scraping & Ingestion:** Fetches real-time web search results and extracts clean text from relevant pages.
3. **Content Summarization:** Produces preliminary summaries on extracted samples to distill high-yield information.
4. **Vector Indexing & RAG:** Embeds the scraped content into a local vector database to build an interactive, context-aware query engine.
5. **Report Compilation:** Uses a local LLM (via **Ollama**) or cloud models to synthesize the retrieved context into a structured markdown report and exports it directly to your designated output file.

---

## 🛠️ Pipeline Architecture

```text
[ User Input: Destination ]
             │
             ▼
 ┌──────────────────────┐
 │  1. Query Generator  │ ──► Generates domain-specific search queries
 └───────────┬──────────┘
             │
             ▼
 ┌──────────────────────┐
 │ 2. Web Search & Scrape│ ──► Retrieves web pages & extracts clean text
 └───────────┬──────────┘
             │
             ▼
 ┌──────────────────────┐
 │ 3. Sample Summarizer │ ──► Distills core insights from raw content
 └───────────┬──────────┘
             │
             ▼
 ┌──────────────────────┐
 │  4. Vector DB & RAG  │ ──► Builds local vector index for deep context retrieval
 └───────────┬──────────┘
             │
             ▼
 ┌──────────────────────┐
 │ 5. Report Generator  │ ──► Local LLM (Ollama) synthesizes final output file
 └──────────────────────┘

