from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import List

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_cerebras import ChatCerebras

from .tools import RetrieverConfig, retrieve_context, format_context


SYSTEM_PROMPT = (
    "You are a helpful assistant answering questions about product specs. "
    "Always use the provided context to ground your answer. "
    "Cite sources in brackets like [1], [2]. Keep answers concise."
)


@dataclass
class Memory:
    messages: List = field(default_factory=list)

    def as_messages(self):
        return list(self.messages)

    def add_user(self, content: str):
        self.messages.append(HumanMessage(content=content))

    def add_ai(self, content: str):
        self.messages.append(AIMessage(content=content))


def run_chat(index_dir: str = "data/index/chroma", collection: str = "rag_mvp") -> None:
    # Init LLM (requires CEREBRAS_API_KEY)
    llm = ChatCerebras(model="gpt-oss-120b")

    mem = Memory()
    retriever_cfg = RetrieverConfig(index_dir=index_dir, collection_name=collection)

    print("Type 'exit' to quit. Ask a question:")
    while True:
        try:
            q = input("> ").strip()
        except EOFError:
            break
        if not q:
            continue
        if q.lower() in {"exit", "quit"}:
            break

        # Always use the RAG tool at least once
        snippets = retrieve_context(q, retriever_cfg)
        ctx = format_context(snippets)

        # Build messages with memory + system + new user message including context
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + mem.as_messages()
        user_msg = (
            f"Question: {q}\n\nContext:\n{ctx}\n\n"
            "Answer using only the context. Include short citations like [1], [2]."
        )
        messages.append(HumanMessage(content=user_msg))

        ai = llm.invoke(messages)
        answer = getattr(ai, "content", str(ai))
        print("\n" + answer + "\n")

        # Update memory
        mem.add_user(q)
        mem.add_ai(answer)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="RAG MVP Chat Agent")
    ap.add_argument("chat", nargs="?", default="chat", help="Start chat session")
    ap.add_argument("--index-dir", default="data/index/chroma")
    ap.add_argument("--collection", default="rag_mvp")
    args = ap.parse_args()
    run_chat(index_dir=args.index_dir, collection=args.collection)

