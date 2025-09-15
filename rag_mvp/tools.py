from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

from langchain_community.vectorstores import Chroma
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings


@dataclass
class RetrieverConfig:
    index_dir: Path = Path("data/index/chroma")
    collection_name: str = "rag_mvp"
    k: int = 5


def get_vectorstore(index_dir: Path, collection_name: str) -> Chroma:
    emb = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return Chroma(
        collection_name=collection_name,
        persist_directory=str(index_dir),
        embedding_function=emb,
    )


def get_retriever(cfg: RetrieverConfig):
    vs = get_vectorstore(cfg.index_dir, cfg.collection_name)
    return vs.as_retriever(search_kwargs={"k": cfg.k})


def retrieve_context(query: str, cfg: RetrieverConfig = RetrieverConfig()) -> List[Dict[str, Any]]:
    retriever = get_retriever(cfg)
    docs = retriever.get_relevant_documents(query)
    results = []
    for d in docs:
        results.append({
            "text": d.page_content,
            "source": d.metadata.get("source"),
            "doc_id": d.metadata.get("doc_id"),
        })
    return results


def format_context(snippets: List[Dict[str, Any]]) -> str:
    lines = []
    for i, s in enumerate(snippets, start=1):
        src = s.get("source") or s.get("doc_id") or "unknown"
        lines.append(f"[{i}] ({src})\n{s.get('text','').strip()}")
    return "\n\n".join(lines)

