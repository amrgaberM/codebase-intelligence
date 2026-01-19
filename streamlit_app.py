import os
import streamlit as st
import time
import shutil
from pathlib import Path
import sys

# ------------------------------
# Disable ChromaDB telemetry
# ------------------------------
os.environ["CHROMA_TELEMETRY"] = "false"

# ------------------------------
# Add src folder to path
# ------------------------------
sys.path.insert(0, str(Path(__file__).parent))

# ------------------------------
# Streamlit page config
# ------------------------------
st.set_page_config(
    page_title="CodeLens - AI Code Intelligence",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# Initialize session state
# ------------------------------
if "retriever" not in st.session_state:
    st.session_state.retriever = None
    st.session_state.generator = None
    st.session_state.reranker = None
    st.session_state.intelligence = None
    st.session_state.indexed = False
    st.session_state.messages = []
    st.session_state.repo_name = ""
    st.session_state.files_count = 0
    st.session_state.chunks_count = 0
    st.session_state.files = None
    st.session_state.show_estimate = False
    st.session_state.estimated_time = 0

# ------------------------------
# Utility functions
# ------------------------------
def clear_database():
    vectors_path = Path("data/vectors")
    repos_path = Path("data/repos")
    if vectors_path.exists():
        shutil.rmtree(vectors_path, ignore_errors=True)
    if repos_path.exists():
        shutil.rmtree(repos_path, ignore_errors=True)
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def estimate_time(repo_url: str) -> dict:
    """Estimate indexing time based on repo size."""
    import requests
    try:
        parts = repo_url.rstrip('/').rstrip('.git').split('/')
        owner, repo = parts[-2], parts[-1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            size_kb = data.get('size', 0)
            est_files = max(10, size_kb // 5)
            est_chunks = est_files * 4
            est_seconds = int(est_chunks * 0.3) + 10
            return {
                "success": True,
                "repo_name": data.get('full_name', f"{owner}/{repo}"),
                "size_kb": size_kb,
                "stars": data.get('stargazers_count', 0),
                "est_files": est_files,
                "est_chunks": est_chunks,
                "est_seconds": est_seconds,
                "est_time_str": f"{est_seconds // 60}m {est_seconds % 60}s" if est_seconds >= 60 else f"{est_seconds}s"
            }
    except Exception:
        pass
    return {"success": False}

def index_repository(repo_url, progress_callback=None):
    from src.ingestion import GitHubLoader
    from src.chunking import ASTChunker
    from src.retrieval import HybridRetriever, LightweightReranker
    from src.generation import CodeGenerator, CodeIntelligence

    if progress_callback:
        progress_callback(10, "Cloning repository...")
    
    loader = GitHubLoader()
    files = loader.clone_repo(repo_url)
    
    if progress_callback:
        progress_callback(30, f"Parsing {len(files)} files...")
    
    chunker = ASTChunker()
    chunks = chunker.chunk_files(files)
    
    if progress_callback:
        progress_callback(50, f"Indexing {len(chunks)} chunks...")
    
    # ------------------------------
    # Telemetry-free retriever
    # ------------------------------
    retriever = HybridRetriever()  # telemetry is disabled via env variable
    generator = CodeGenerator()
    reranker = LightweightReranker()
    retriever.index(chunks, files)
    
    if progress_callback:
        progress_callback(90, "Building intelligence...")
    
    intelligence = CodeIntelligence(retriever, generator)
    
    return {
        "files": files,
        "chunks": chunks,
        "retriever": retriever,
        "generator": generator,
        "reranker": reranker,
        "intelligence": intelligence,
        "repo_name": loader._parse_repo_name(repo_url)
    }

# ------------------------------
# Sidebar UI
# ------------------------------
with st.sidebar:
    st.markdown("### CodeLens")
    st.markdown('<p style="color: #64748b; font-size: 0.875rem;">AI-Powered Code Intelligence</p>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown('<p style="color: #e2e8f0; font-weight: 500; margin-bottom: 0.5rem;">Repository URL</p>', unsafe_allow_html=True)
    repo_url = st.text_input("GitHub URL", placeholder="https://github.com/owner/repo", label_visibility="collapsed")
    
    if repo_url and not st.session_state.get("indexed", False):
        if st.button("Estimate Time", key="estimate_btn", use_container_width=True):
            with st.spinner("Checking repository..."):
                estimate = estimate_time(repo_url)
                if estimate["success"]:
                    st.session_state.show_estimate = True
                    st.session_state.estimate_data = estimate
                else:
                    st.warning("Could not fetch repo info. Try indexing directly.")
        
        if st.session_state.get("show_estimate", False) and "estimate_data" in st.session_state:
            est = st.session_state.estimate_data
            st.markdown(f"""
            <div class="estimate-box">
                <div class="estimate-label">Estimated Time</div>
                <div class="estimate-time">{est['est_time_str']}</div>
                <div class="estimate-label" style="margin-top: 0.5rem;">
                    ~{est['est_files']} files | ~{est['est_chunks']} chunks | {est['size_kb']} KB
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        index_btn = st.button("Index", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("Clear", type="secondary", use_container_width=True)
    
    if clear_btn:
        clear_database()
        st.rerun()
    
    if index_btn and repo_url:
        try:
            clear_database()
            
            progress_bar = st.progress(0, text="Starting...")
            status_text = st.empty()
            
            def update_progress(pct, text):
                progress_bar.progress(pct, text=text)
                status_text.markdown(f'<p style="color: #94a3b8; font-size: 0.8rem;">{text}</p>', unsafe_allow_html=True)
            
            start_time = time.time()
            result = index_repository(repo_url, update_progress)
            elapsed = time.time() - start_time
            
            progress_bar.progress(100, text="Complete!")
            status_text.markdown(f'<p style="color: #10b981; font-size: 0.8rem;">Completed in {elapsed:.1f}s</p>', unsafe_allow_html=True)
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
            
            st.session_state.files = result["files"]
            st.session_state.retriever = result["retriever"]
            st.session_state.generator = result["generator"]
            st.session_state.reranker = result["reranker"]
            st.session_state.intelligence = result["intelligence"]
            st.session_state.repo_name = result["repo_name"]
            st.session_state.files_count = len(result["files"])
            st.session_state.chunks_count = len(result["chunks"])
            st.session_state.indexed = True
            st.session_state.messages = []
            st.session_state.show_estimate = False
            
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ------------------------------
# Main content UI
# ------------------------------
# Here you can paste your original HTML/CSS, chat tabs, and all features
# They will continue to work with telemetry-disabled retriever
