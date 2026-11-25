"""Core logic for the document Q&A bot: load a PDF, index it, answer with page citations.

Chat model: DeepSeek (OpenAI-compatible API).
Embeddings: any OpenAI-compatible embeddings endpoint (Ollama locally, or Qwen/DashScope).
Settings come from the .env file in the repository root.
"""
import logging
import os
import re

from dotenv import find_dotenv, load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv(find_dotenv(usecwd=True))

logger = logging.getLogger(__name__)

NOT_FOUND = "文档中没有找到相关内容。 / I couldn't find this in the document."

SYSTEM_PROMPT = (
    "You answer questions using ONLY the context passages below, taken from one document. "
    "Each passage starts with its page tag, for example [p.3].\n"
    "Rules:\n"
    "1. Answer in the same language as the question. Keep it concise.\n"
    "2. After each fact, cite the page tag it came from, for example [p.3].\n"
    "3. If the passages do not contain the answer, reply exactly: " + NOT_FOUND + "\n"
    "4. Never use outside knowledge and never guess."
)

PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "Context:\n{context}\n\nQuestion: {question}"),
])


def _env(name: str, default: str | None = None) -> str:
    value = os.getenv(name) or default
    if not value:
        raise RuntimeError(f"Set {name} in the .env file (see .env.example).")
    return value


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=_env("DEEPSEEK_MODEL", "deepseek-chat"),
        api_key=_env("DEEPSEEK_API_KEY"),
        base_url=_env("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        temperature=0,
        timeout=60,
        max_retries=3,
    )


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=_env("EMBED_MODEL"),
        base_url=_env("EMBED_BASE_URL"),
        api_key=os.getenv("EMBED_API_KEY") or "not-needed",  # Ollama ignores the key
        check_embedding_ctx_length=False,  # send plain text, not OpenAI token arrays
        chunk_size=int(os.getenv("EMBED_BATCH", "10")),  # DashScope accepts at most 10 per call
    )


def load_pdf(path: str):
    """Read a PDF and split it into chunks that remember their page number (1-based)."""
    pages = PyPDFLoader(path).load()
    for doc in pages:
        doc.metadata["page_number"] = int(doc.metadata.get("page", 0)) + 1
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n\n", "\n", "。", "！", "？", ". ", "；", "; ", " ", ""],
    )
    chunks = splitter.split_documents(pages)
    return [c for c in chunks if c.page_content.strip()]


def build_index(chunks) -> InMemoryVectorStore:
    store = InMemoryVectorStore(get_embeddings())
    store.add_documents(chunks)
    return store


def is_not_found(text: str) -> bool:
    return "没有找到相关内容" in text or "couldn't find this" in text.lower()


def rewrite_query(question: str, llm) -> str:
    """Add a Chinese search query for English questions; preserve the original."""
    if re.search(r"[\u3400-\u9fff]", question) or not re.search(r"[A-Za-z]", question):
        return question
    try:
        reply = llm.invoke([
            ("system", "Translate the user's search question into concise Simplified Chinese. "
             "Preserve its meaning, names, numbers and constraints. Do not answer the question. "
             "Return only the translated question, without commentary."),
            ("human", question),
        ])
        translated = reply.content.strip()
        if translated and re.search(r"[\u3400-\u9fff]", translated):
            return f"{question}\n{translated}"
    except Exception as exc:
        logger.warning("Query rewrite failed (%s); using original question.", type(exc).__name__)
    return question


def retrieve(store, question: str, llm, k: int = 4):
    """Search the bilingual query and retain original-query evidence as well."""
    query = rewrite_query(question, llm)
    if query == question:
        return store.similarity_search(question, k=k)
    hits = store.similarity_search(query, k=k)
    original_hits = store.similarity_search(question, k=k)
    unique = {}
    for doc in hits + original_hits:
        key = (doc.metadata["page_number"], doc.page_content)
        unique.setdefault(key, doc)
    return list(unique.values())


def answer(store: InMemoryVectorStore, question: str, k: int = 4) -> dict:
    llm = get_llm()
    hits = retrieve(store, question, llm, k=k)
    context = "\n\n".join(f"[p.{d.metadata['page_number']}] {d.page_content}" for d in hits)
    reply = (PROMPT | llm).invoke({"context": context, "question": question})
    text = reply.content.strip()
    cited = sorted({int(p) for p in re.findall(r"\[p\.(\d+)\]", text)})
    return {
        "answer": text,
        "found": not is_not_found(text),
        "cited_pages": cited,
        "sources": [{"page": d.metadata["page_number"], "text": d.page_content} for d in hits],
    }
