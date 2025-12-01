from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional

from langchain_community.vectorstores import Chroma
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings

from rag_mvp.mongo_store import get_mongo_client, get_mongo_db, get_mongo_collection


@dataclass
class RetrieverConfig:
    index_dir: Path = Path("data/index/chroma")
    collection_name: str = "rag_mvp"
    k: int = 5


def get_vectorstore(index_dir: Path, collection_name: str) -> Chroma:
    emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return Chroma(
        collection_name=collection_name,
        persist_directory=str(index_dir),
        embedding_function=emb,
    )


def get_retriever(cfg: RetrieverConfig):
    vs = get_vectorstore(cfg.index_dir, cfg.collection_name)
    return vs.as_retriever(search_kwargs={"k": cfg.k})


def retrieve_context(
        query: str,
        cfg: RetrieverConfig = RetrieverConfig(),
        *,
        k: Optional[int] = None,
        filt: Optional[Dict[str, Any]] = None,
        where: Optional[str] = None,
        contains: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    # Set up MongoDB connection
    client = get_mongo_client()
    db = get_mongo_db(client)
    collection = get_mongo_collection(db, cfg.collection_name)

    # Use vectorstore directly to support passing filter at query-time
    vs = get_vectorstore(cfg.index_dir, cfg.collection_name)
    kk = k or cfg.k
    # First-stage retrieval
    if filt or where:
        docs = vs.similarity_search(query, k=max(kk * 4, 20), filter=filt, where_document={"$contains": where})
    else:
        docs = vs.similarity_search(query, k=max(kk * 4, 20))
    # Optional contains-based metadata filtering at app layer (substring, case-insensitive)
    if contains:
        def ok(d) -> bool:
            for key, needle in contains.items():
                hay = (d.metadata or {}).get(key)
                if not isinstance(hay, str):
                    return False
                if needle.lower() not in hay.lower():
                    return False
            return True

        docs = [d for d in docs if ok(d)]
    # Trim to k
    docs = docs[:kk]
    results = []
    for d in docs:
        results.append({
            "text": d.page_content,
            "source": (d.metadata or {}).get("source"),
            "doc_id": (d.metadata or {}).get("doc_id"),
            "metadata": d.metadata or {},
        })

    client.close()
    return results


def format_context(snippets: List[Dict[str, Any]]) -> str:
    lines = []
    for i, s in enumerate(snippets, start=1):
        src = s.get("source") or s.get("doc_id") or "unknown"
        lines.append(f"[{i}] ({src})\n{s.get('text', '').strip()}")
    return "\n\n".join(lines)
