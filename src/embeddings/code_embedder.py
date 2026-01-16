from typing import List, Optional, Union
import numpy as np
from logger import logger


class CodeEmbedder:
    
    def __init__(self, model_name: Optional[str] = None):
        # Use a smaller, faster model
        self.model_name = model_name or "all-MiniLM-L6-v2"
        self._model = None
        logger.info(f"Embedder initialized with model: {self.model_name}")
    
    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            
            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
            # Force CPU to avoid GPU memory issues
            self._model = self._model.to('cpu')
        return self._model
    
    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()
    
    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]
        
        # Smaller batch size for memory efficiency
        embeddings = self.model.encode(
            texts,
            show_progress_bar=False,
            normalize_embeddings=True,
            batch_size=32,
            convert_to_numpy=True
        )
        return embeddings
    
    def embed_query(self, query: str) -> np.ndarray:
        return self.embed(query)[0]
    
    def embed_documents(self, documents: List[str]) -> np.ndarray:
        return self.embed(documents)
