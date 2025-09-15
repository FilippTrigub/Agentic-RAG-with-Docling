from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any

from langchain_cerebras import ChatCerebras
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import StructuredTool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from .tools import RetrieverConfig, retrieve_context


SYSTEM_PROMPT = (
    "You are a helpful assistant answering questions about product specs. "
    "Use the RAG tool to retrieve relevant context BEFORE answering. "
    "If tool use did not yield relevant information, try again with adjusted filters and query. "
    "You may try up to 10 times. "
    "Cite sources in brackets like [1], [2]. Keep answers concise.\n\n"
    "Metadata fields are simple strings (substring searchable), for example: \n"
    "product_features_and_benefits, areas_of_application, general_product_information, electrical_data, photometric_data, physical_attributes_dimensions, operating_conditions, product_datasheet, environmental_regulatory_information.\n"
    "When users mention product numbers, lamp base, or application, pass a 'contains' filter to the tool."
)


# Store meta about the last tool call for UX printing
LAST_TOOL_CALL: Dict[str, Any] = {"snippets": []}


class RetrieveInput(BaseModel):
    query: str = Field(..., description="User's natural language query")
    k: int = Field(5, description="Number of documents to retrieve")
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Exact metadata filter (use sparingly).",
    )
    contains: Optional[Dict[str, str]] = Field(
        default=None,
        description=(
            "Substring filters over metadata, e.g., {'general_product_information':'SIRIUS', 'areas_of_application':'Microscopy'}"
        ),
    )


def make_retrieve_tool(cfg: RetrieverConfig) -> StructuredTool:
    def _impl(
        query: str,
        k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        contains: Optional[Dict[str, str]] = None,
    ) -> str:
        global LAST_TOOL_CALL
        snippets = retrieve_context(query, cfg, k=k, filt=filters, contains=contains)
        LAST_TOOL_CALL = {"snippets": snippets, "k": k, "filters": filters or {}, "contains": contains or {}}
        # Return readable context for the model
        lines = [f"[Tool] retrieve_context hits={len(snippets)}"]
        for i, s in enumerate(snippets, start=1):
            src = s.get("source") or s.get("doc_id") or "unknown"
            lines.append(f"[{i}] {src}")
        lines.append("")
        for i, s in enumerate(snippets, start=1):
            lines.append(f"[{i}]\n{s.get('text','').strip()}")
            lines.append("")
        return "\n".join(lines).strip()

    return StructuredTool.from_function(
        name="retrieve_context",
        description=(
            "Retrieve relevant document snippets from the product spec index. "
            "Always call this at least once before answering. Accepts optional metadata filters."
        ),
        func=_impl,
        args_schema=RetrieveInput,
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
    retriever_cfg = RetrieverConfig(index_dir=Path(index_dir), collection_name=collection)

    # Build tool and agentic RAG
    tool = make_retrieve_tool(retriever_cfg)
    tools = [tool]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        return_intermediate_steps=True,
        verbose=False,
    )

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

        inputs = {"input": q, "chat_history": mem.as_messages()}
        result = executor.invoke(inputs)
        answer = result.get("output", "")

        # Augment output with tool usage and sources
        snippets = LAST_TOOL_CALL.get("snippets", [])
        hits = len(snippets)
        print(f"\n[Tool] retrieve_context used; hits={hits}")
        print("\n" + answer + "\n")
        if hits:
            src_lines = []
            for i, s in enumerate(snippets, start=1):
                src = s.get("source") or s.get("doc_id") or "unknown"
                src_lines.append(f"[{i}] {src}")
            print("Sources:\n" + "\n".join(src_lines))
            print(f"Hits: {hits}\n")

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
