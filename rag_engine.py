"""
rag_engine.py
-------------
RAG (Retrieval-Augmented Generation) engine for myAdvisr.

Architecture:
  1. INDEXING   — on first run, embed all documents → store in ChromaDB
  2. RETRIEVAL  — at query time, embed query → cosine similarity search → top-k chunks
  3. INJECTION  — retrieved chunks injected into Claude's system prompt as grounding context

Libraries:
  - chromadb           : local vector database (no API key needed, runs in-process)
  - sentence-transformers: creates embeddings using a local model
"""

import os
import streamlit as st
from knowledge_base import DOCUMENTS


# ── Constants ────────────────────────────────────────────────────────────────
COLLECTION_NAME  = "myadvisr_kb"
EMBEDDING_MODEL  = "all-MiniLM-L6-v2"   # fast, 384-dim, great for semantic search
TOP_K            = 5                      # number of chunks to retrieve per query
SIMILARITY_THRESHOLD = 1.8               # ChromaDB uses L2 distance; lower = more similar


# ── Initialise the RAG engine (cached so it only runs once per session) ──────
@st.cache_resource(show_spinner=False)
def init_rag():
    """
    Load the embedding model and build/load the ChromaDB vector store.
    Returns (collection, embedding_model).
    Cached by Streamlit so this runs once per app session.
    """
    import chromadb
    from sentence_transformers import SentenceTransformer

    # Load the embedding model (downloads ~90 MB on first run, cached afterwards)
    model = SentenceTransformer(EMBEDDING_MODEL)

    # ChromaDB in-memory client (ephemeral — rebuilds each session)
    # For persistence across restarts use: chromadb.PersistentClient(path="./chroma_db")
    client = chromadb.Client()

    # Create or get existing collection
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception:
        collection = client.create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}   # use cosine similarity
        )

    # Index documents if collection is empty
    if collection.count() == 0:
        texts    = [doc["text"]     for doc in DOCUMENTS]
        ids      = [doc["id"]       for doc in DOCUMENTS]
        metadatas= [doc["metadata"] for doc in DOCUMENTS]

        # Create embeddings in one batch
        embeddings = model.encode(texts, show_progress_bar=False).tolist()

        collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )

    return collection, model


def retrieve(query: str, student_profile: dict = None, top_k: int = TOP_K) -> list[dict]:
    """
    Retrieve the most relevant knowledge base chunks for a given query.

    Args:
        query          : the student's question or message
        student_profile: optional dict with major, level, careers etc for query enrichment
        top_k          : number of chunks to return

    Returns:
        list of dicts with keys: id, text, metadata, distance, relevance_score
    """
    collection, model = init_rag()

    # Enrich query with student context so retrieval is more targeted
    enriched_query = query
    if student_profile:
        major   = student_profile.get("major", "")
        level   = student_profile.get("level", "")
        careers = ", ".join(student_profile.get("careers", []))
        if major or careers:
            enriched_query = f"{query} [Student context: {level} {major} interested in {careers}]"

    # Embed the query
    query_embedding = model.encode([enriched_query], show_progress_bar=False).tolist()

    # Search the vector store
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    # Format results
    chunks = []
    if results and results["documents"]:
        for i, (doc, meta, dist) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )):
            relevance = round((1 - dist) * 100, 1)   # convert distance → 0-100 score
            chunks.append({
                "id":              results["ids"][0][i],
                "text":            doc,
                "metadata":        meta,
                "distance":        dist,
                "relevance_score": relevance,
            })

    return chunks


def build_rag_context(chunks: list[dict]) -> str:
    """
    Format retrieved chunks into a clean context string to inject into Claude's prompt.
    """
    if not chunks:
        return ""

    lines = ["=== RETRIEVED KNOWLEDGE BASE CONTEXT ===",
             "The following information was retrieved from the Clarkson University",
             "knowledge base and is directly relevant to the student's question.",
             "Use this information to ground your response in accurate, specific facts.",
             ""]

    for i, chunk in enumerate(chunks, 1):
        cat = chunk["metadata"].get("category", "info").upper()
        score = chunk["relevance_score"]
        lines.append(f"[{i}] [{cat}] (relevance: {score}%)")
        lines.append(chunk["text"])
        lines.append("")

    lines.append("=== END RETRIEVED CONTEXT ===")
    return "\n".join(lines)


def retrieve_and_format(query: str, student_profile: dict = None) -> str:
    """
    Convenience function: retrieve relevant chunks and return formatted context string.
    Call this right before each Claude API request.
    """
    chunks = retrieve(query, student_profile=student_profile)
    return build_rag_context(chunks)


def get_index_stats() -> dict:
    """Return stats about the knowledge base for display in the UI."""
    try:
        collection, _ = init_rag()
        return {
            "total_documents": collection.count(),
            "model":           EMBEDDING_MODEL,
            "status":          "ready",
        }
    except Exception as e:
        return {"total_documents": 0, "model": EMBEDDING_MODEL, "status": f"error: {e}"}
