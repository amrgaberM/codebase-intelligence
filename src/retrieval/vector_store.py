"""Vector store implementation using ChromaDB."""

from pathlib import Path
from typing import Dict, List, Optional, Any
import json

import chromadb

from ..chunking import CodeChunk
from ..embeddings import CodeEmbedder
from ..utils import config, logger


class VectorStore:
    """Vector store for code chunks using ChromaDB."""
    
    def __init__(
        self,
        collection_name: Optional[str] = None,
        persist_directory: Optional[str] = None,
        embedder: Optional[CodeEmbedder] = None,
    ):
        """Initialize vector store.
        
        Args:
            collection_name: Name for the ChromaDB collection
            persist_directory: Directory to persist the database
            embedder: Embedder instance for generating embeddings
        """
        self.collection_name = collection_name or config.get(
            "vector_store.collection_name", "codebase"
        )
        self.persist_directory = persist_directory or config.get(
            "vector_store.persist_directory", "./data/vectors"
        )
        
        # Ensure directory exists
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize embedder
        self.embedder = embedder or CodeEmbedder()
        
        # Initialize ChromaDB
        self._client = None
        self._collection = None
        
        logger.info(f"VectorStore initialized: {self.collection_name}")
    
    @property
    def client(self) -> chromadb.ClientAPI:
        """Lazy load ChromaDB client."""
        if self._client is None:
            self._client = chromadb.PersistentClient(
                path=self.persist_directory,
            )
        return self._client
    
    @property
    def collection(self) -> chromadb.Collection:
        """Get or create collection."""
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}  # Use cosine similarity
            )
        return self._collection
    
    def add_chunks(self, chunks: List[CodeChunk], batch_size: int = 100) -> None:
        """Add chunks to the vector store.
        
        Args:
            chunks: List of CodeChunk objects
            batch_size: Number of chunks to process at once
        """
        if not chunks:
            logger.warning("No chunks to add")
            return
        
        logger.info(f"Adding {len(chunks)} chunks to vector store")
        
        # Process in batches
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            
            # Prepare data
            ids = [chunk.chunk_id for chunk in batch]
            documents = [chunk.to_embedding_text() for chunk in batch]
            metadatas = [self._prepare_metadata(chunk) for chunk in batch]
            
            # Generate embeddings
            embeddings = self.embedder.embed_documents(documents)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings.tolist(),
                documents=documents,
                metadatas=metadatas,
            )
            
            logger.debug(f"Added batch {i // batch_size + 1}")
        
        logger.info(f"✅ Successfully added {len(chunks)} chunks")
    
    def search(
        self,
        query: str,
        top_k: int = 10,
        filter_dict: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        """Search for relevant chunks.
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of results with chunk data and scores
        """
        # Generate query embedding
        query_embedding = self.embedder.embed_query(query)
        
        # Build where clause
        where = filter_dict if filter_dict else None
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        
        # Format results
        formatted = []
        for i in range(len(results["ids"][0])):
            formatted.append({
                "chunk_id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "score": 1 - results["distances"][0][i],  # Convert distance to similarity
            })
        
        return formatted
    
    def delete_collection(self) -> None:
        """Delete the entire collection."""
        self.client.delete_collection(self.collection_name)
        self._collection = None
        logger.info(f"Deleted collection: {self.collection_name}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        return {
            "name": self.collection_name,
            "count": self.collection.count(),
        }
    
    def _prepare_metadata(self, chunk: CodeChunk) -> Dict[str, Any]:
        """Prepare metadata for ChromaDB (must be flat)."""
        # ChromaDB requires flat metadata (no nested dicts/lists)
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
        
        # Flatten some metadata
        if chunk.metadata.get("repo_name"):
            metadata["repo_name"] = chunk.metadata["repo_name"]
        if chunk.metadata.get("docstring"):
            metadata["docstring"] = chunk.metadata["docstring"][:500]  # Limit size
        
        # Convert imports to string (ChromaDB doesn't support lists)
        if chunk.imports:
            metadata["imports"] = ",".join(chunk.imports[:20])
        
        return metadata