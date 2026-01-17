import streamlit as st
import time
import shutil
from pathlib import Path
import sys

# Add path for local imports (preserving your logic)
sys.path.insert(0, str(Path(__file__).parent))

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CodeLens | AI Code Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# PROFESSIONAL UI & CSS STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Variables & Reset */
    :root {
        --primary: #6366f1;
        --secondary: #8b5cf6;
        --accent: #06b6d4;
        --bg-dark: #0f1117;
        --bg-card: rgba(30, 41, 59, 0.7);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --border: rgba(148, 163, 184, 0.1);
    }
    
    /* App Background */
    .stApp {
        background: radial-gradient(circle at top left, #1e1b4b 0%, #0f1117 40%);
        color: var(--text-primary);
    }

    /* Modern Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99, 102, 241, 0.3); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99, 102, 241, 0.6); }

    /* Typography */
    h1, h2, h3 { font-family: 'Inter', sans-serif; letter-spacing: -0.02em; }
    
    /* Custom Classes for UI Elements */
    .hero-container {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(180deg, rgba(99, 102, 241, 0.1) 0%, transparent 100%);
        border-radius: 24px;
        margin-bottom: 3rem;
        border: 1px solid var(--border);
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        max-width: 600px;
        margin: 0 auto;
    }

    /* Glass Cards */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }

    /* Icon Box */
    .icon-box {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    /* Stats HUD */
    .hud-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .hud-item {
        flex: 1;
        background: linear-gradient(90deg, rgba(30, 41, 59, 0.8) 0%, rgba(30, 41, 59, 0.4) 100%);
        border-left: 4px solid var(--primary);
        padding: 1rem;
        border-radius: 0 12px 12px 0;
        min-width: 150px;
    }

    .hud-value { font-size: 1.5rem; font-weight: 700; color: #fff; }
    .hud-label { font-size: 0.75rem; text-transform: uppercase; color: var(--text-secondary); letter-spacing: 0.05em; }

    /* Steps Timeline */
    .step-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px dashed var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        position: relative;
    }
    .step-badge {
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--primary);
        color: white;
        font-weight: bold;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid var(--border);
    }
    
    /* Input Fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }

    /* Buttons */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        border: none;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    .stButton button[kind="secondary"] {
        background: transparent;
        border: 1px solid var(--border);
        color: var(--text-secondary);
    }
    .stButton button:hover {
        transform: translateY(-1px);
        opacity: 0.9;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border: none;
        color: var(--text-secondary);
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: var(--primary);
        border-bottom: 2px solid var(--primary);
    }

    /* Custom Source Item */
    .source-item {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        font-family: 'SF Mono', 'Roboto Mono', monospace;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .source-item:before {
        content: '';
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--accent);
    }

    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE & HELPERS
# -----------------------------------------------------------------------------
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
    except Exception as e:
        pass
    return {"success": False}

def index_repository(repo_url, progress_callback=None):
    # NOTE: Assuming these imports exist in your environment as per original code
    from src.ingestion import GitHubLoader
    from src.chunking import ASTChunker
    from src.retrieval import HybridRetriever, LightweightReranker
    from src.generation import CodeGenerator, CodeIntelligence
    
    if progress_callback: progress_callback(10, "Cloning repository...")
    loader = GitHubLoader()
    files = loader.clone_repo(repo_url)
    
    if progress_callback: progress_callback(30, f"Parsing {len(files)} files...")
    chunker = ASTChunker()
    chunks = chunker.chunk_files(files)
    
    if progress_callback: progress_callback(50, f"Indexing {len(chunks)} chunks...")
    retriever = HybridRetriever()
    generator = CodeGenerator()
    reranker = LightweightReranker()
    retriever.index(chunks, files)
    
    if progress_callback: progress_callback(90, "Building intelligence...")
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

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ CodeLens")
    st.markdown('<p style="color: #64748b; font-size: 0.8rem; margin-top: -10px;">AI-Powered Code Intelligence</p>', unsafe_allow_html=True)
    st.divider()
    
    st.caption("REPOSITORY SETUP")
    repo_url = st.text_input("GitHub URL", placeholder="https://github.com/owner/repo", label_visibility="collapsed")
    
    col_est, col_idx = st.columns(2)
    
    # Estimate Logic
    if repo_url and not st.session_state.get("indexed", False):
        with col_est:
            if st.button("Estimate", key="estimate_btn", use_container_width=True):
                with st.spinner("..."):
                    estimate = estimate_time(repo_url)
                    if estimate["success"]:
                        st.session_state.show_estimate = True
                        st.session_state.estimate_data = estimate
                    else:
                        st.warning("Failed")
    
    # Display Estimate in Sidebar if available
    if st.session_state.get("show_estimate", False) and "estimate_data" in st.session_state:
        est = st.session_state.estimate_data
        st.markdown(f"""
        <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px; padding: 12px; margin: 10px 0;">
            <div style="color: #a5b4fc; font-weight: bold; font-size: 1.1rem;">⏱ {est['est_time_str']}</div>
            <div style="color: #94a3b8; font-size: 0.75rem;">{est['est_files']} files • {est['size_kb']} KB</div>
        </div>
        """, unsafe_allow_html=True)

    # Indexing Logic
    if repo_url:
        with col_idx:
            index_btn = st.button("Index", type="primary", use_container_width=True)
            
        if index_btn:
            try:
                clear_database()
                progress_bar = st.progress(0, text="Initializing...")
                status_box = st.empty()
                
                def update_progress(pct, text):
                    progress_bar.progress(pct, text=text)
                    status_box.caption(f"✨ {text}")
                
                start_time = time.time()
                result = index_repository(repo_url, update_progress)
                elapsed = time.time() - start_time
                
                progress_bar.progress(100, text="Ready!")
                status_box.success(f"Done in {elapsed:.1f}s")
                time.sleep(1)
                progress_bar.empty()
                status_box.empty()
                
                # Update State
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

    if st.session_state.get("indexed", False):
        st.divider()
        if st.button("Reset / Clear", type="secondary", use_container_width=True):
            clear_database()
            st.rerun()
            
        st.divider()
        st.caption("SEARCH SETTINGS")
        top_k = st.slider("Context Window (Chunks)", 1, 10, 5)
        use_reranking = st.checkbox("Semantic Reranking", value=True)
    else:
        top_k = 5
        use_reranking = True

# -----------------------------------------------------------------------------
# MAIN CONTENT
# -----------------------------------------------------------------------------

# --- VIEW: LANDING PAGE (NOT INDEXED) ---
if not st.session_state.get("indexed", False):
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">CodeLens</h1>
        <p class="hero-subtitle">Decode any repository in seconds. <br>AI-powered semantic search, analysis, and documentation generation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Grid
    c1, c2, c3, c4 = st.columns(4)
    
    features = [
        {"icon": "💬", "title": "Natural QA", "desc": "Chat with your codebase in plain English."},
        {"icon": "🔍", "title": "Deep Search", "desc": "Hybrid semantic & keyword retrieval."},
        {"icon": "🔗", "title": "Dependency", "desc": "Trace logic across files and classes."},
        {"icon": "⚡", "title": "AST Parsing", "desc": "Structure-aware code chunking."}
    ]
    
    for col, feat in zip([c1, c2, c3, c4], features):
        with col:
            st.markdown(f"""
            <div class="glass-card">
                <div class="icon-box">{feat['icon']}</div>
                <h3 style="font-size: 1rem; margin-bottom: 0.5rem; color: #f1f5f9;">{feat['title']}</h3>
                <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.5;">{feat['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Workflow Section
    st.markdown('<h2 style="text-align: center; margin: 4rem 0 2rem;">How It Works</h2>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    
    steps = [
        {"num": "01", "title": "Paste URL", "desc": "Enter a public GitHub repository URL in the sidebar."},
        {"num": "02", "title": "Index Code", "desc": "Our AI analyzes structure, syntax trees, and semantics."},
        {"num": "03", "title": "Interact", "desc": "Ask questions, generate docs, or analyze functions."}
    ]
    
    for col, step in zip([s1, s2, s3], steps):
        with col:
            st.markdown(f"""
            <div class="step-card">
                <div class="step-badge">{step['num']}</div>
                <h3 style="font-size: 1.1rem; margin-bottom: 0.5rem; color: #e2e8f0;">{step['title']}</h3>
                <p style="font-size: 0.9rem; color: #64748b;">{step['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Suggested Repos
    st.markdown('<div style="margin-top: 3rem;"></div>', unsafe_allow_html=True)
    st.caption("POPULAR REPOSITORIES TO TRY")
    r1, r2, r3 = st.columns(3)
    
    repos = [
        {"name": "tiangolo/typer", "type": "CLI Framework"},
        {"name": "psf/requests", "type": "HTTP Library"},
        {"name": "pallets/flask", "type": "Web Framework"}
    ]
    
    for col, repo in zip([r1, r2, r3], repos):
        with col:
            st.code(f"github.com/{repo['name']}")

# --- VIEW: DASHBOARD (INDEXED) ---
else:
    # Header & HUD
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1rem;">
        <div>
            <h1 style="margin: 0; background: linear-gradient(to right, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{st.session_state.get("repo_name", "Repository")}</h1>
            <p style="color: #64748b; margin: 0;">Active Intelligence Session</p>
        </div>
    </div>
    
    <div class="hud-container">
        <div class="hud-item">
            <div class="hud-value">{st.session_state.get("files_count", 0)}</div>
            <div class="hud-label">Source Files</div>
        </div>
        <div class="hud-item">
            <div class="hud-value">{st.session_state.get("chunks_count", 0)}</div>
            <div class="hud-label">Knowledge Chunks</div>
        </div>
        <div class="hud-item" style="border-left-color: var(--accent);">
            <div class="hud-value">Ready</div>
            <div class="hud-label">System Status</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat", "⚡ Explain", "🔍 Similar", "📝 Docs", "📊 Analyze"])
    
    # --- TAB 1: CHAT ---
    with tab1:
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        # Chat History
        for msg in st.session_state.get("messages", []):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("sources"):
                    with st.expander("📚 Referenced Sources"):
                        for src in msg["sources"]:
                            st.markdown(f'<div class="source-item">{src}</div>', unsafe_allow_html=True)
        
        # Input
        if prompt := st.chat_input("Ask about the codebase logic, structure, or implementation..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing code vectors..."):
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
                            answer = "No relevant code found. Try a different question."
                        
                        elapsed = time.time() - start
                    except Exception as e:
                        answer = f"Error: {str(e)}"
                        results = []
                        elapsed = 0
                
                st.markdown(answer)
                
                sources = []
                if results:
                    with st.expander("📚 Referenced Sources"):
                        for i, r in enumerate(results[:5], 1):
                            meta = r.get("metadata", {})
                            src_text = f"{meta.get('file_path', '?')} : {meta.get('name', '?')}"
                            sources.append(src_text)
                            st.markdown(f"""
                            <div class="source-item">
                                <b>{i}.</b> {src_text} 
                                <span style="opacity: 0.5; margin-left: auto;">{meta.get('chunk_type', 'code')}</span>
                            </div>
                            """, unsafe_allow_html=True)
                
                st.caption(f"Generated in {elapsed:.2f}s")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

    # --- TAB 2: EXPLAIN ---
    with tab2:
        col_ex1, col_ex2 = st.columns([1, 1])
        with col_ex1:
            func_name = st.text_input("Target Name", placeholder="e.g. UserModel, process_data")
        with col_ex2:
            file_path = st.text_input("File Context (Optional)", placeholder="src/models.py")
            
        if st.button("Generate Explanation", type="primary", use_container_width=True):
            if func_name:
                with st.spinner("Analysing AST and Logic..."):
                    try:
                        intelligence = st.session_state.get("intelligence")
                        result = intelligence.explain_function(func_name, file_path if file_path else None)
                        
                        if "error" in result:
                            st.warning(result["error"])
                        else:
                            st.markdown(f"### 💡 {result['function_name']}")
                            st.caption(f"📍 {result['file_path']} : Lines {result.get('start_line', '?')}-{result.get('end_line', '?')}")
                            
                            st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
                            st.markdown(result["explanation"])
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            with st.expander("Show Original Code"):
                                st.code(result["code"], language="python")
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")

    # --- TAB 3: SIMILAR ---
    with tab3:
        code_snippet = st.text_area("Reference Code", placeholder="Paste a function or logic pattern here...", height=200)
        
        if st.button("Find Matches", type="primary"):
            if code_snippet:
                with st.spinner("Computing vector similarity..."):
                    try:
                        intelligence = st.session_state.get("intelligence")
                        results = intelligence.find_similar_code(code_snippet, top_k=5)
                        
                        if results:
                            for i, r in enumerate(results, 1):
                                st.markdown(f"""
                                <div class="glass-card" style="margin-bottom: 1rem;">
                                    <div style="display: flex; justify-content: space-between;">
                                        <h4 style="margin:0;">{r['name']}</h4>
                                        <span style="color: var(--accent);">Match: {r['similarity_score']:.3f}</span>
                                    </div>
                                    <p style="color: #94a3b8; font-size: 0.8rem;">{r['file']} | Line {r['line']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                with st.expander(f"View Code: {r['name']}"):
                                    st.code(r["code"], language="python")
                        else:
                            st.info("No similar patterns found.")
                    except Exception as e:
                        st.error(str(e))

    # --- TAB 4: DOCS ---
    with tab4:
        files = st.session_state.get("files", [])
        file_paths = [f.path for f in files] if files else []
        
        selected_file = st.selectbox("Select Target File", file_paths if file_paths else ["No files"])
        
        if st.button("Generate Documentation", key="docs_btn"):
            if selected_file and selected_file != "No files":
                with st.spinner("Drafting documentation..."):
                    try:
                        intelligence = st.session_state.get("intelligence")
                        docs = intelligence.generate_documentation(selected_file)
                        st.markdown(docs)
                    except Exception as e:
                        st.error(str(e))

    # --- TAB 5: ANALYZE ---
    with tab5:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Full Codebase Scan", use_container_width=True):
                with st.spinner("Scanning structure..."):
                    try:
                        intelligence = st.session_state.get("intelligence")
                        stats = intelligence.analyze_codebase()
                        st.session_state.codebase_stats = stats
                    except Exception as e:
                        st.error(str(e))
        with c2:
            if st.button("Find Symbol Usages", use_container_width=True):
                st.session_state.show_usage_input = True

        if "codebase_stats" in st.session_state:
            stats = st.session_state.codebase_stats
            
            st.markdown("### Structural Overview")
            sc1, sc2, sc3 = st.columns(3)
            with sc1: st.metric("Total Files", stats.get('total_files', 0))
            with sc2: st.metric("Code Chunks", stats.get('total_chunks', 0))
            with sc3: st.metric("Defined Classes", len(stats.get('classes', [])))
            
            st.markdown("---")
            d1, d2 = st.columns(2)
            with d1:
                st.subheader("Classes")
                for cls in stats.get("classes", [])[:10]:
                    st.markdown(f'<div class="source-item">📦 {cls["name"]} <span style="color: #64748b; margin-left: auto;">{cls["file"]}</span></div>', unsafe_allow_html=True)
            with d2:
                st.subheader("Functions")
                for func in stats.get("functions", [])[:10]:
                    st.markdown(f'<div class="source-item">🔧 {func["name"]} <span style="color: #64748b; margin-left: auto;">{func["file"]}</span></div>', unsafe_allow_html=True)

        if st.session_state.get("show_usage_input", False):
            st.divider()
            usage_name = st.text_input("Enter symbol name", key="usage_input", placeholder="e.g. BaseLoader")
            if st.button("Trace Usages"):
                with st.spinner("Tracing..."):
                    try:
                        intelligence = st.session_state.get("intelligence")
                        usages = intelligence.find_usages(usage_name)
                        st.success(f"Found {usages['total_usages']} occurrences")
                        
                        udata = usages.get("usages", {})
                        if udata.get("definition"):
                            d = udata["definition"]
                            st.markdown(f"**Definition:** `{d['file']}:{d['line']}`")
                        
                        if udata.get("calls"):
                            st.markdown("**References:**")
                            for call in udata["calls"][:10]:
                                st.markdown(f"- `{call['file']}` at line {call['line']}")
                    except Exception as e:
                        st.error(str(e))
