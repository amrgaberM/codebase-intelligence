"""Gradio UI for CodeBase Intelligence RAG."""

import gradio as gr
import time
from typing import List, Tuple

from src.ingestion import GitHubLoader
from src.chunking import ASTChunker
from src.retrieval import HybridRetriever, LightweightReranker
from src.generation import CodeGenerator
from src.utils import logger

# Global state
retriever = None
generator = None
reranker = None
indexed_repos = []


def initialize_system():
    """Initialize the RAG system components."""
    global retriever, generator, reranker
    
    if retriever is None:
        retriever = HybridRetriever()
    if generator is None:
        generator = CodeGenerator()
    if reranker is None:
        reranker = LightweightReranker()
    
    return retriever, generator, reranker


def ingest_repo(repo_url: str, progress=gr.Progress()) -> str:
    """Ingest a repository."""
    global indexed_repos
    
    if not repo_url:
        return "❌ Please enter a repository URL"
    
    try:
        progress(0.1, desc="Initializing...")
        retriever, _, _ = initialize_system()
        
        progress(0.2, desc="Cloning repository...")
        loader = GitHubLoader()
        files = loader.clone_repo(repo_url)
        
        if not files:
            return "❌ No files found in repository"
        
        progress(0.5, desc=f"Chunking {len(files)} files...")
        chunker = ASTChunker()
        chunks = chunker.chunk_files(files)
        
        progress(0.7, desc=f"Indexing {len(chunks)} chunks...")
        retriever.index(chunks)
        
        repo_name = loader._parse_repo_name(repo_url)
        indexed_repos.append(repo_name)
        
        progress(1.0, desc="Done!")
        
        return f"""✅ **Successfully indexed!**
        
📦 **Repository:** {repo_name}
📄 **Files processed:** {len(files)}
🧩 **Chunks created:** {len(chunks)}

You can now ask questions about the codebase!"""
        
    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        return f"❌ Error: {str(e)}"


def query_codebase(
    query: str,
    top_k: int,
    use_reranking: bool,
    history: List[Tuple[str, str]]
) -> Tuple[List[Tuple[str, str]], str]:
    """Query the codebase and return response."""
    
    if history is None:
        history = []
    
    if not query:
        return history, ""
    
    if retriever is None:
        history.append((query, "❌ Please ingest a repository first!"))
        return history, ""
    
    try:
        # Retrieve
        start = time.time()
        results = retriever.search(query, top_k=top_k * 2)
        
        if not results:
            history.append((query, "No relevant code found. Try a different query."))
            return history, ""
        
        # Rerank
        if use_reranking:
            results = reranker.rerank(query, results, top_k=top_k)
        else:
            results = results[:top_k]
        
        retrieval_time = time.time() - start
        
        # Generate
        start = time.time()
        answer = generator.generate(query, results)
        generation_time = time.time() - start
        
        # Format sources
        sources = []
        for i, r in enumerate(results[:3], 1):
            meta = r.get("metadata", {})
            sources.append(
                f"{i}. `{meta.get('file_path', 'unknown')}` "
                f"({meta.get('chunk_type', 'code')}: {meta.get('name', 'unnamed')})"
            )
        
        sources_text = "\n".join(sources)
        
        full_response = f"""{answer}

---
📚 **Sources:**
{sources_text}

⏱️ Retrieval: {retrieval_time*1000:.0f}ms | Generation: {generation_time*1000:.0f}ms"""
        
        history.append((query, full_response))
        return history, ""
        
    except Exception as e:
        logger.error(f"Query error: {e}")
        history.append((query, f"❌ Error: {str(e)}"))
        return history, ""


def clear_chat():
    """Clear chat history."""
    return [], ""


# Build Gradio UI
with gr.Blocks(
    title="CodeBase Intelligence RAG",
    theme=gr.themes.Soft(),
) as demo:
    
    gr.Markdown("""
    # 🧠 CodeBase Intelligence RAG
    
    **Upload any GitHub repository and chat with it!**
    
    1. Enter a GitHub repo URL and click "Ingest"
    2. Ask questions about the codebase
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📦 Repository")
            
            repo_url = gr.Textbox(
                label="GitHub URL",
                placeholder="https://github.com/owner/repo",
            )
            
            ingest_btn = gr.Button("🔄 Ingest Repository", variant="primary")
            
            ingest_status = gr.Markdown("")
            
            gr.Markdown("### ⚙️ Settings")
            
            top_k = gr.Slider(
                minimum=1,
                maximum=10,
                value=5,
                step=1,
                label="Number of chunks to retrieve",
            )
            
            use_reranking = gr.Checkbox(
                value=True,
                label="Use reranking",
            )
        
        with gr.Column(scale=2):
            gr.Markdown("### 💬 Chat")
            
            chatbot = gr.Chatbot(
                height=400,
                show_label=False,
            )
            
            with gr.Row():
                query_input = gr.Textbox(
                    label="Ask a question",
                    placeholder="How does authentication work?",
                    scale=4,
                )
                
                send_btn = gr.Button("Send", variant="primary", scale=1)
            
            clear_btn = gr.Button("🗑️ Clear Chat")
    
    # Event handlers
    ingest_btn.click(
        fn=ingest_repo,
        inputs=[repo_url],
        outputs=[ingest_status],
    )
    
    send_btn.click(
        fn=query_codebase,
        inputs=[query_input, top_k, use_reranking, chatbot],
        outputs=[chatbot, query_input],
    )
    
    query_input.submit(
        fn=query_codebase,
        inputs=[query_input, top_k, use_reranking, chatbot],
        outputs=[chatbot, query_input],
    )
    
    clear_btn.click(
        fn=clear_chat,
        outputs=[chatbot, query_input],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)