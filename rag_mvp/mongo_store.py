from __future__ import annotations

import os
from typing import Any, Dict, List

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


def get_mongo_client() -> MongoClient:
    """Returns a MongoClient instance."""
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    return MongoClient(mongo_uri)


def get_mongo_db(client: MongoClient, db_name: str = "rag_mvp") -> Database:
    """Returns a Database instance."""
    return client[db_name]


def get_mongo_collection(
    db: Database, collection_name: str = "documents"
) -> Collection:
    """Returns a Collection instance."""
    return db[collection_name]


def insert_documents(collection: Collection, documents: List[Dict[str, Any]]) -> None:
    """Inserts a list of documents into a collection."""
    collection.insert_many(documents)

