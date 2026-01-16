from typing import List, Optional, Union
import numpy as np
from ..utils import config, logger


class CodeEmbedder:
    
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or "BAAI/bge-base-en-v1.5"
        self._model = None
        logger.info(f"Embedder initialized with model: {self.model_name}")
    
    @property
    def model(self):
        if self._model is None:
            import torch
            from sentence_transformers import SentenceTransformer
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Loading embedding model: {self.model_name} on {device.upper()}")
            
            self._model = SentenceTransformer(self.model_name, device=device)
        return self._model
    
    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()
    
    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(
            texts,
            show_progress_bar=len(texts) > 10,
            normalize_embeddings=True,
            batch_size=64,
        )
        return embeddings
    
    def embed_query(self, query: str) -> np.ndarray:
        return self.embed(query)[0]
    
    def embed_documents(self, documents: List[str]) -> np.ndarray:
        return self.embed(documents)
