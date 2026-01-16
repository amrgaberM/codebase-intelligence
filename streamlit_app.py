import streamlit as st
import time
import shutil
from pathlib import Path

st.set_page_config(
    page_title="CodeLens",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #64748B;
        margin-top: 0.5rem;
    }
    
    .source-item {
        background: #F8FAFC;
        border-left: 3px solid #667eea;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 0.85rem;
    }
    
    .feature-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .success-banner {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        font-weight: 500;
    }
    
    div[data-testid="stChatMessage"] {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
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
    st.session_state.indexing = False

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
    from src.ingestion import GitHubLoader
    from src.chunking import ASTChunker
    from src.retrieval import HybridRetriever, LightweightReranker
    from src.generation import CodeGenerator, CodeIntelligence
    
    loader = GitHubLoader()
    files = loader.clone_repo(repo_url)
    
    chunker = ASTChunker()
    chunks = chunker.chunk_files(files)
    
    retriever = HybridRetriever()
    generator = CodeGenerator()
    reranker = LightweightReranker()
    retriever.index(chunks, files)
    
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

# Sidebar
with st.sidebar:
    st.markdown("## CodeLens")
    st.markdown("AI-Powered Code Intelligence")
    
    st.divider()
    
    st.markdown("### Repository")
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
            
            progress_bar = st.progress(0, text="Starting...")
            
            progress_bar.progress(10, text="Cloning repository...")
            result = index_repository(repo_url)
            
            progress_bar.progress(100, text="Complete!")
            time.sleep(0.5)
            progress_bar.empty()
            
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
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    if st.session_state.indexed:
        st.divider()
        st.markdown("### Statistics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Files", st.session_state.files_count)
        with col2:
            st.metric("Chunks", st.session_state.chunks_count)
        
        st.caption(f" {st.session_state.repo_name}")
        
        st.divider()
        st.markdown("### Settings")
        top_k = st.slider("Results", 1, 10, 5)
        use_reranking = st.checkbox("Reranking", value=True)
    else:
        top_k = 5
        use_reranking = True
    
    st.divider()
    st.markdown(
        "<div style='text-align:center; color:#94A3B8; font-size:0.75rem;'>"
        "Built with Streamlit + LangChain<br>GPU Accelerated"
        "</div>",
        unsafe_allow_html=True
    )

# Main content
if not st.session_state.indexed:
    # Landing page
    st.markdown('<p class="main-header">CodeLens</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Understand any codebase in seconds with AI-powered intelligence</p>', unsafe_allow_html=True)
    
    st.divider()
    
    # Features
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number"></div>
            <div class="stat-label">Natural Language Q&A</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number"></div>
            <div class="stat-label">Smart Code Search</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number"></div>
            <div class="stat-label">Dependency Analysis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number"></div>
            <div class="stat-label">Auto Documentation</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # How it works
    st.markdown("### How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">1</div>
            <strong>Paste GitHub URL</strong><br>
            <span style="color:#64748B">Enter any public repository URL in the sidebar</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">2</div>
            <strong>Click Index</strong><br>
            <span style="color:#64748B">AI analyzes and understands the entire codebase</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">3</div>
            <strong>Ask Anything</strong><br>
            <span style="color:#64748B">Chat naturally about the code structure and logic</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Example repos
    st.markdown("### Try These Repositories")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.code("https://github.com/tiangolo/typer", language=None)
        st.caption("CLI Framework")
    
    with col2:
        st.code("https://github.com/psf/requests", language=None)
        st.caption("HTTP Library")
    
    with col3:
        st.code("https://github.com/pallets/flask", language=None)
        st.caption("Web Framework")

else:
    # Indexed state - show tabs
    st.markdown(f'<p class="main-header">CodeLens</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Analyzing: {st.session_state.repo_name}</p>', unsafe_allow_html=True)
    
    tabs = st.tabs([" Chat", " Explain", " Find Usages", " Generate Docs", " Analysis"])
    
    # Tab 1: Chat
    with tabs[0]:
        # Chat messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("sources"):
                    with st.expander("View Sources"):
                        for src in msg["sources"]:
                            st.markdown(f'<div class="source-item">{src}</div>', unsafe_allow_html=True)
        
        # Chat input
        if prompt := st.chat_input("Ask about the codebase..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        start = time.time()
                        results = st.session_state.retriever.search(prompt, top_k=top_k*2)
                        
                        if results and use_reranking:
                            results = st.session_state.reranker.rerank(prompt, results, top_k=top_k)
                        elif results:
                            results = results[:top_k]
                        
                        if results:
                            answer = st.session_state.generator.generate(prompt, results)
                        else:
                            answer = "No relevant code found. Try a different question."
                        
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
                            src = f"{meta.get('file_path', '?')}  {meta.get('name', '?')} ({meta.get('chunk_type', '?')})"
                            sources.append(src)
                            st.markdown(f'<div class="source-item">{i}. {src}</div>', unsafe_allow_html=True)
                
                st.caption(f" {elapsed:.2f}s")
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
    
    # Tab 2: Explain
    with tabs[1]:
        st.markdown("### Explain Function or Class")
        
        func_name = st.text_input("Enter name", placeholder="e.g., main, get_user, Config")
        
        if st.button("Explain", key="explain_btn", type="primary"):
            if func_name:
                with st.spinner("Analyzing..."):
                    result = st.session_state.intelligence.explain_function(func_name)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"**File:** {result['file_path']}")
                        st.markdown(f"**Lines:** {result['start_line']} - {result['end_line']}")
                    
                    st.code(result["code"], language="python")
                    st.markdown("### Explanation")
                    st.markdown(result["explanation"])
    
    # Tab 3: Find Usages
    with tabs[2]:
        st.markdown("### Find Usages")
        
        search_name = st.text_input("Enter name to find", placeholder="e.g., config, User, db")
        
        if st.button("Search", key="usage_btn", type="primary"):
            if search_name:
                with st.spinner("Searching..."):
                    result = st.session_state.intelligence.find_usages(search_name)
                
                st.markdown(f"**Found {result['total_usages']} occurrences**")
                
                usages = result["usages"]
                
                if usages["definition"]:
                    st.markdown("#### Definition")
                    d = usages["definition"]
                    st.markdown(f'<div class="source-item">{d["file"]} (line {d["line"]})</div>', unsafe_allow_html=True)
                
                if usages["calls"]:
                    st.markdown("#### Calls")
                    for u in usages["calls"][:10]:
                        st.markdown(f'<div class="source-item">{u["file"]} (line {u["line"]})</div>', unsafe_allow_html=True)
    
    # Tab 4: Generate Docs
    with tabs[3]:
        st.markdown("### Generate Documentation")
        
        if st.session_state.files:
            py_files = [f.path for f in st.session_state.files if f.language == "python"]
            selected = st.selectbox("Select file", py_files)
            
            if st.button("Generate", key="docs_btn", type="primary"):
                with st.spinner("Generating documentation..."):
                    docs = st.session_state.intelligence.generate_documentation(selected)
                
                st.markdown(docs)
                
                st.download_button(
                    "Download Markdown",
                    docs,
                    file_name=f"{Path(selected).stem}_docs.md",
                    mime="text/markdown"
                )
    
    # Tab 5: Analysis
    with tabs[4]:
        st.markdown("### Codebase Analysis")
        
        if st.button("Analyze", key="analyze_btn", type="primary"):
            with st.spinner("Analyzing codebase..."):
                stats = st.session_state.intelligence.analyze_codebase()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Files", stats["total_files"])
            with col2:
                st.metric("Chunks", stats["total_chunks"])
            with col3:
                st.metric("Classes", len(stats["classes"]))
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Classes")
                for c in stats["classes"][:10]:
                    st.markdown(f'<div class="source-item">{c["name"]} in {c["file"]}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### Functions")
                for f in stats["functions"][:10]:
                    st.markdown(f'<div class="source-item">{f["name"]} in {f["file"]}</div>', unsafe_allow_html=True)
