from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable, List, Any, Dict

from langchain_core.documents import Document
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings


def _iter_json_files(processed_dir: Path) -> Iterable[Path]:
    yield from processed_dir.glob("*.json")


def _norm_key(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def _clean_item(v: Any) -> Any:
    if isinstance(v, str):
        return v.lstrip("_•- ").strip()
    return v


def _flatten_for_metadata(record: Dict[str, Any], path: Path) -> Dict[str, Any]:
    md: Dict[str, Any] = {
        "source": record.get("source") or str(path),
        "doc_id": path.stem,
    }
    for k, v in record.items():
        if k == "content":
            continue
        nk = _norm_key(k)
        if isinstance(v, dict):
            for dk, dv in v.items():
                md[f"kv.{nk}.{_norm_key(dk)}"] = _clean_item(dv)
        elif isinstance(v, list):
            # Join list items into a single string to satisfy Chroma's metadata type constraints
            str_items = [_clean_item(x) for x in v if isinstance(x, str)]
            if str_items:
                md[f"list.{nk}"] = " | ".join(str_items)
                # Also index each item as a boolean flag for exact filtering
                for item in str_items:
                    md[f"list_item.{nk}.{_norm_key(item)}"] = True
            # If list contains dicts, flatten with indices as a best-effort
            for i, elem in enumerate(v):
                if isinstance(elem, dict):
                    for dk, dv in elem.items():
                        md[f"kv.{nk}[{i}].{_norm_key(dk)}"] = _clean_item(dv)
        else:
            md[f"kv.{nk}"] = _clean_item(v)
    return md


def _load_documents(processed_dir: Path) -> List[Document]:
    docs: List[Document] = []
    for p in _iter_json_files(processed_dir):
        try:
            # Validate JSON first to fail fast with helpful errors
            json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        loader = JSONLoader(
            file_path=str(p),
            jq_schema=".",            # load the entire JSON object
            content_key="content",     # use 'content' field as page_content
            text_content=False,
            metadata_func=(lambda rec, _metadata=None, _p=p: _flatten_for_metadata(rec, _p)),
        )
        try:
            loaded = loader.load()
        except Exception:
            # Fallback to manual if loader fails for any reason
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                content = (data.get("content") or "").strip()
                if not content:
                    continue
                docs.append(
                    Document(
                        page_content=content,
                        metadata={
                            "source": str(p),
                            "doc_id": p.stem,
                        },
                    )
                )
                continue
            except Exception:
                continue
        # Expect one document per JSON file
        for d in loaded:
            if d.page_content and d.page_content.strip():
                docs.append(d)
    return docs


def build_index(
    processed_dir: Path = Path("data/processed"),
    index_dir: Path = Path("data/index/chroma"),
    collection_name: str = "rag_mvp",
) -> int:
    """Build a Chroma index from processed JSON files.

    Returns the number of documents added.
    Requires GOOGLE_API_KEY in the environment for embeddings.
    """
    processed_dir.mkdir(parents=True, exist_ok=True)
    index_dir.mkdir(parents=True, exist_ok=True)

    docs = _load_documents(processed_dir)
    if not docs:
        return 0

    emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vs = Chroma(
        collection_name=collection_name,
        persist_directory=str(index_dir),
        embedding_function=emb,
    )

    vs.add_documents(docs)
    vs.persist()
    return len(docs)


def load_vectorstore(
    index_dir: Path = Path("data/index/chroma"),
    collection_name: str = "rag_mvp",
):
    emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return Chroma(
        collection_name=collection_name,
        persist_directory=str(index_dir),
        embedding_function=emb,
    )


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Build Chroma index from processed JSON")
    ap.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--index-dir", type=Path, default=Path("data/index/chroma"))
    ap.add_argument("--collection", type=str, default="rag_mvp")
    args = ap.parse_args()

    n = build_index(args.processed_dir, args.index_dir, args.collection)
    print(f"Indexed {n} documents into {args.index_dir}")
