"""Fast embeddings using local SentenceTransformers with code-optimized model."""

from typing import List, Union
import numpy as np
from src.utils.logger import logger


class CodeEmbedder:
    """Embeddings optimized for code using BGE model (512 token context)."""
    
    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5"):
        """
        Initialize embedder.
        
        Model options:
        - "BAAI/bge-base-en-v1.5" (768 dim, 512 tokens) - RECOMMENDED for code
        - "all-MiniLM-L6-v2" (384 dim, 256 tokens) - Faster but less context
        - "all-mpnet-base-v2" (768 dim, 384 tokens) - Good balance
        """
        self.model_name = model_name
        self._model = None
        self._dimension = 768 if "bge" in model_name or "mpnet" in model_name else 384
        logger.info(f"Embedder initialized: {self.model_name} ({self._dimension} dim)")
    
    @property
    def model(self):
        """Lazy load the model."""
        if self._model is None:
            logger.info(f"Loading embedding model: {self.model_name}...")
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
            logger.info("Embedding model loaded")
        return self._model
    
    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        """Embed text(s) into vectors."""
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=32,  # Smaller batch for larger model
            show_progress_bar=False,
        )
        
        return np.array(embeddings)
    
    def embed_query(self, query: str) -> np.ndarray:
        """Embed a single query with instruction prefix for BGE."""
        # BGE models perform better with this prefix for queries
        if "bge" in self.model_name.lower():
            query = f"Represent this code question: {query}"
        return self.embed(query)[0]
    
    def embed_documents(self, documents: List[str]) -> np.ndarray:
        """Embed multiple documents efficiently."""
        if not documents:
            return np.array([])
        
        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=len(documents) > 200,
        )
        
        return np.array(embeddings)
    
    @property
    def dimension(self) -> int:
        """Embedding dimension."""
        return self._dimension
