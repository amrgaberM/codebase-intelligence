from typing import List, Optional, Union
import numpy as np
import os
import requests
from logger import logger


class CodeEmbedder:
    """Fast embeddings using HuggingFace Inference API (free)."""
    
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or "sentence-transformers/all-MiniLM-L6-v2"
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{self.model_name}"
        self.headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN', '')}"}
        self._local_model = None
        logger.info(f"Embedder initialized: {self.model_name}")
    
    def _embed_api(self, texts: List[str]) -> Optional[np.ndarray]:
        """Try HuggingFace API first (faster)."""
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": texts, "options": {"wait_for_model": True}},
                timeout=60
            )
            if response.status_code == 200:
                embeddings = np.array(response.json())
                norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
                return embeddings / norms
        except Exception as e:
            logger.warning(f"API failed, using local model: {e}")
        return None
    
    def _embed_local(self, texts: List[str]) -> np.ndarray:
        """Fallback to local model."""
        if self._local_model is None:
            from sentence_transformers import SentenceTransformer
            self._local_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        return self._local_model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=False
        )
    
    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]
        
        result = self._embed_api(texts)
        if result is not None:
            return result
        
        return self._embed_local(texts)
    
    def embed_query(self, query: str) -> np.ndarray:
        return self.embed(query)[0]
    
    def embed_documents(self, documents: List[str]) -> np.ndarray:
        batch_size = 50
        all_embeddings = []
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            embeddings = self.embed(batch)
            all_embeddings.append(embeddings)
        
        return np.vstack(all_embeddings)
    
    @property
    def dimension(self) -> int:
        return 384
