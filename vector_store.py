"""Vector store implementation using ChromaDB."""

from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import shutil

import chromadb

from base_chunker import CodeChunk
from code_embedder import CodeEmbedder
from config import config
from logger import logger


class VectorStore:
    """Vector store for code chunks using ChromaDB."""
    
    def __init__(
        self,
        collection_name: Optional[str] = None,
        persist_directory: Optional[str] = None,
        embedder: Optional[CodeEmbedder] = None,
    ):
        self.collection_name = collection_name or config.get(
            "vector_store.collection_name", "codebase"
        )
        self.persist_directory = persist_directory or config.get(
            "vector_store.persist_directory", "./data/vectors"
        )
        
        # Clear old corrupted data if exists
        vectors_path = Path(self.persist_directory)
        if vectors_path.exists():
            shutil.rmtree(vectors_path, ignore_errors=True)
        
        self.embedder = embedder or CodeEmbedder()
        self._client = None
        self._collection = None
        
        logger.info(f"VectorStore initialized: {self.collection_name}")
    
    @property
    def client(self) -> chromadb.ClientAPI:
        if self._client is None:
            self._client = chromadb.EphemeralClient()
        return self._client
    
    @property
    def collection(self) -> chromadb.Collection:
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        return self._collection
    
    def add_chunks(self, chunks: List[CodeChunk], batch_size: int = 100) -> None:
        if not chunks:
            logger.warning("No chunks to add")
            return
        
        logger.info(f"Adding {len(chunks)} chunks to vector store")
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            ids = [chunk.chunk_id for chunk in batch]
            documents = [chunk.to_embedding_text() for chunk in batch]
            metadatas = [self._prepare_metadata(chunk) for chunk in batch]
            embeddings = self.embedder.embed_documents(documents)
            
            self.collection.add(
                ids=ids,
                embeddings=embeddings.tolist(),
                documents=documents,
                metadatas=metadatas,
            )
            logger.debug(f"Added batch {i // batch_size + 1}")
        
        logger.info(f"Successfully added {len(chunks)} chunks")
    
    def search(
        self,
        query: str,
        top_k: int = 10,
        filter_dict: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        query_embedding = self.embedder.embed_query(query)
        where = filter_dict if filter_dict else None
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        
        formatted = []
        for i in range(len(results["ids"][0])):
            formatted.append({
                "chunk_id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "score": 1 - results["distances"][0][i],
            })
        
        return formatted
    
    def delete_collection(self) -> None:
        try:
            self.client.delete_collection(self.collection_name)
        except:
            pass
        self._collection = None
        logger.info(f"Deleted collection: {self.collection_name}")
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "name": self.collection_name,
            "count": self.collection.count(),
        }
    
    def _prepare_metadata(self, chunk: CodeChunk) -> Dict[str, Any]:
        metadata = {
            "file_path": chunk.file_path,
            "chunk_type": chunk.chunk_type,
            "language": chunk.language,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
        }
        
        if chunk.name:
            metadata["name"] = chunk.name
        if chunk.parent:
            metadata["parent"] = chunk.parent
        if chunk.metadata.get("repo_name"):
            metadata["repo_name"] = chunk.metadata["repo_name"]
        if chunk.metadata.get("docstring"):
            metadata["docstring"] = chunk.metadata["docstring"][:500]
        if chunk.imports:
            metadata["imports"] = ",".join(chunk.imports[:20])
        
        return metadata
