import streamlit as st
import time
import shutil
from pathlib import Path

st.set_page_config(
    page_title="CodeLens - AI Code Intelligence",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .sub-title {
        font-size: 1.25rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-box {
        background: rgba(30, 30, 50, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-box:hover {
        border-color: rgba(99, 102, 241, 0.5);
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15);
    }
    
    .feature-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-size: 1.5rem;
        color: white;
    }
    
    .feature-title {
        font-size: 1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.875rem;
        color: #64748b;
        line-height: 1.5;
    }
    
    .step-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .step-box {
        background: rgba(30, 30, 50, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        flex: 1;
        max-width: 300px;
    }
    
    .step-number {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-weight: 700;
        color: white;
        font-size: 1.1rem;
    }
    
    .step-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }
    
    .step-desc {
        font-size: 0.875rem;
        color: #64748b;
    }
    
    .repo-card {
        background: rgba(30, 30, 50, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .repo-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .repo-url {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #a5b4fc;
        background: rgba(99, 102, 241, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
        word-break: break-all;
    }
    
    .repo-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #e2e8f0;
        text-align: center;
        margin: 3rem 0 2rem;
    }
    
    .chat-header {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    
    .chat-subheader {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    
    .source-item {
        background: rgba(99, 102, 241, 0.1);
        border-left: 3px solid #6366f1;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #cbd5e1;
    }
    
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-box {
        background: rgba(99, 102, 241, 0.1);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        flex: 1;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #a5b4fc;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
    }
    
    section[data-testid="stSidebar"] {
        background: rgba(15, 15, 35, 0.95);
        border-right: 1px solid rgba(99, 102, 241, 0.1);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }
    
    .stTextInput input {
        background: rgba(30, 30, 50, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 8px;
        color: #e2e8f0;
        padding: 0.75rem 1rem;
    }
    
    .stTextInput input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
    }
    
    .stButton > button[kind="secondary"] {
        background: transparent;
        border: 1px solid rgba(99, 102, 241, 0.5);
        color: #a5b4fc;
    }
    
    .stChatMessage {
        background: rgba(30, 30, 50, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.1);
        border-radius: 12px;
        padding: 1rem;
    }
    
    .stChatInputContainer {
        background: rgba(30, 30, 50, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
    }
    
    .stSlider {
        color: #a5b4fc;
    }
    
    .streamlit-expanderHeader {
        background: rgba(99, 102, 241, 0.1);
        border-radius: 8px;
        color: #e2e8f0;
    }
    
    [data-testid="stMetricValue"] {
        color: #a5b4fc;
    }
    
    [data-testid="stMetricLabel"] {
        color: #64748b;
    }
    
    .stProgress > div > div {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    hr {
        border-color: rgba(99, 102, 241, 0.1);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "retriever" not in st.session_state:
    st.session_state.retriever = None
    st.session_state.generator = None
    st.session_state.reranker = None
    st.session_state.indexed = False
    st.session_state.messages = []
    st.session_state.repo_name = ""
    st.session_state.files_count = 0
    st.session_state.chunks_count = 0
    st.session_state.files = None

def clear_database():
    vectors_path = Path("data/vectors")
    repos_path = Path("data/repos")
    if vectors_path.exists():
        shutil.rmtree(vectors_path, ignore_errors=True)
    if repos_path.exists():
        shutil.rmtree(repos_path, ignore_errors=True)
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def index_repository(repo_url):
    import sys
    sys.path.insert(0, '.')
    
    from github_loader import GitHubLoader
    from ast_chunker import ASTChunker
    from hybrid_retriever import HybridRetriever
    from reranker import LightweightReranker
    from generator import CodeGenerator
    
    loader = GitHubLoader()
    files = loader.clone_repo(repo_url)
    
    chunker = ASTChunker()
    chunks = chunker.chunk_files(files)
    
    retriever = HybridRetriever()
    generator = CodeGenerator()
    reranker = LightweightReranker()
    retriever.index(chunks)
    
    return {
        "files": files,
        "chunks": chunks,
        "retriever": retriever,
        "generator": generator,
        "reranker": reranker,
        "repo_name": loader._parse_repo_name(repo_url)
    }

# Sidebar
with st.sidebar:
    st.markdown("### CodeLens")
    st.markdown('<p style="color: #64748b; font-size: 0.875rem;">AI-Powered Code Intelligence</p>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown('<p style="color: #e2e8f0; font-weight: 500; margin-bottom: 0.5rem;">Repository URL</p>', unsafe_allow_html=True)
    repo_url = st.text_input(
        "GitHub URL",
        placeholder="https://github.com/owner/repo",
        label_visibility="collapsed"
    )
    
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
            
            progress_bar = st.progress(0, text="Initializing...")
            
            progress_bar.progress(20, text="Cloning repository...")
            result = index_repository(repo_url)
            
            progress_bar.progress(100, text="Complete")
            time.sleep(0.3)
            progress_bar.empty()
            
            st.session_state.files = result["files"]
            st.session_state.retriever = result["retriever"]
            st.session_state.generator = result["generator"]
            st.session_state.reranker = result["reranker"]
            st.session_state.repo_name = result["repo_name"]
            st.session_state.files_count = len(result["files"])
            st.session_state.chunks_count = len(result["chunks"])
            st.session_state.indexed = True
            st.session_state.messages = []
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    if st.session_state.get("indexed", False):
        st.divider()
        st.markdown('<p style="color: #e2e8f0; font-weight: 500;">Statistics</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-box">
                <div class="stat-value">{st.session_state.get("files_count", 0)}</div>
                <div class="stat-label">Files</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{st.session_state.get("chunks_count", 0)}</div>
                <div class="stat-label">Chunks</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f'<p style="color: #64748b; font-size: 0.8rem; margin-top: 0.5rem;">{st.session_state.get("repo_name", "")}</p>', unsafe_allow_html=True)
        
        st.divider()
        st.markdown('<p style="color: #e2e8f0; font-weight: 500;">Settings</p>', unsafe_allow_html=True)
        top_k = st.slider("Number of results", 1, 10, 5)
        use_reranking = st.checkbox("Enable reranking", value=True)
    else:
        top_k = 5
        use_reranking = True

# Main content
if not st.session_state.get("indexed", False):
    st.markdown('<h1 class="main-title">CodeLens</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Understand any codebase in seconds with AI-powered intelligence</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-box">
            <div class="feature-icon">Q</div>
            <div class="feature-title">Natural Language Q&A</div>
            <div class="feature-desc">Ask questions about code in plain English and get precise answers</div>
        </div>
        <div class="feature-box">
            <div class="feature-icon">S</div>
            <div class="feature-title">Smart Code Search</div>
            <div class="feature-desc">Hybrid search combining semantic understanding and keyword matching</div>
        </div>
        <div class="feature-box">
            <div class="feature-icon">D</div>
            <div class="feature-title">Dependency Analysis</div>
            <div class="feature-desc">Understand how files and functions connect across the codebase</div>
        </div>
        <div class="feature-box">
            <div class="feature-icon">A</div>
            <div class="feature-title">AST-Based Chunking</div>
            <div class="feature-desc">Intelligent code parsing that understands structure, not just text</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">How It Works</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="step-container">
        <div class="step-box">
            <div class="step-number">1</div>
            <div class="step-title">Paste Repository URL</div>
            <div class="step-desc">Enter any public GitHub repository URL in the sidebar</div>
        </div>
        <div class="step-box">
            <div class="step-number">2</div>
            <div class="step-title">Click Index</div>
            <div class="step-desc">AI analyzes the entire codebase structure and semantics</div>
        </div>
        <div class="step-box">
            <div class="step-number">3</div>
            <div class="step-title">Ask Questions</div>
            <div class="step-desc">Chat naturally about code structure, logic, and implementation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">Try These Repositories</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="repo-card">
            <div class="repo-url">github.com/tiangolo/typer</div>
            <div class="repo-label">CLI Framework</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="repo-card">
            <div class="repo-url">github.com/psf/requests</div>
            <div class="repo-label">HTTP Library</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="repo-card">
            <div class="repo-url">github.com/pallets/flask</div>
            <div class="repo-label">Web Framework</div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown('<h1 class="chat-header">CodeLens</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="chat-subheader">Analyzing: {st.session_state.get("repo_name", "")}</p>', unsafe_allow_html=True)
    
    for msg in st.session_state.get("messages", []):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("View Sources"):
                    for src in msg["sources"]:
                        st.markdown(f'<div class="source-item">{src}</div>', unsafe_allow_html=True)
    
    if prompt := st.chat_input("Ask about the codebase..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    start = time.time()
                    retriever = st.session_state.get("retriever")
                    generator = st.session_state.get("generator")
                    reranker = st.session_state.get("reranker")
                    
                    results = retriever.search(prompt, top_k=top_k*2)
                    
                    if results and use_reranking:
                        results = reranker.rerank(prompt, results, top_k=top_k)
                    elif results:
                        results = results[:top_k]
                    
                    if results:
                        answer = generator.generate(prompt, results)
                    else:
                        answer = "No relevant code found for your question. Please try rephrasing or ask about a different aspect of the codebase."
                    
                    elapsed = time.time() - start
                except Exception as e:
                    answer = f"Error: {str(e)}"
                    results = []
                    elapsed = 0
            
            st.markdown(answer)
            
            sources = []
            if results:
                with st.expander("View Sources"):
                    for i, r in enumerate(results[:5], 1):
                        meta = r.get("metadata", {})
                        src = f"{meta.get('file_path', 'Unknown')} : {meta.get('name', 'Unknown')} ({meta.get('chunk_type', 'code')})"
                        sources.append(src)
                        st.markdown(f'<div class="source-item">{i}. {src}</div>', unsafe_allow_html=True)
            
            st.caption(f"Response time: {elapsed:.2f}s")
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
