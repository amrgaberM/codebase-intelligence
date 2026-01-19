import streamlit as st
import time
import shutil
from pathlib import Path
import sys

# Add path for local imports
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
# SVG ICONS
# -----------------------------------------------------------------------------
SVGS = {
    "zap": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>""",
    "search": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" x1="21" x2="16.65" y2="16.65"></line></svg>""",
    "chat": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>""",
    "git": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="3" x2="6" y2="15"></line><circle cx="18" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><path d="M18 9a9 9 0 0 1-9 9"></path></svg>""",
    "code": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>""",
    "file": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>""",
    "layers": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>""",
    "box": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>"""
}

# -----------------------------------------------------------------------------
# PROFESSIONAL UI & CSS STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --primary: #6366f1;
        --secondary: #4f46e5;
        --bg-main: #0a0b10;
        --bg-card: rgba(17, 24, 39, 0.7);
        --border-color: rgba(255, 255, 255, 0.08);
        --text-muted: #94a3b8;
    }

    .stApp {
        background-color: var(--bg-main);
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.1) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.05) 0px, transparent 50%);
        color: #f8fafc;
    }

    /* Hide redundant elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Typography */
    h1, h2, h3 { font-family: 'Inter', sans-serif; }
    code, pre { font-family: 'JetBrains Mono', monospace !important; }

    /* Hero & Landing */
    .hero-container {
        padding: 6rem 2rem;
        text-align: center;
        max-width: 900px;
        margin: 0 auto;
    }
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1.1;
        background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-muted);
        line-height: 1.6;
    }

    /* Professional Card UI */
    .glass-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        transition: border 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.3);
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #0d0f14;
        border-right: 1px solid var(--border-color);
        padding: 1.5rem 0.5rem;
    }
    
    /* HUD Stats */
    .hud-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .hud-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border-color);
        padding: 1rem;
        border-radius: 10px;
        text-align: left;
    }
    .hud-value { font-size: 1.5rem; font-weight: 700; color: #fff; }
    .hud-label { font-size: 0.7rem; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.1em; }

    /* Chat Viewport & Formatting */
    .chat-status-bar {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.8rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        border-bottom: 1px solid var(--border-color);
        gap: 24px;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 0;
        background: transparent !important;
        border: none !important;
        color: var(--text-muted) !important;
        font-weight: 500;
        font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        color: #fff !important;
        border-bottom: 2px solid var(--primary) !important;
    }

    /* Buttons */
    .stButton button {
        border-radius: 8px;
        height: 42px;
        transition: 0.2s;
    }
    .stButton button[kind="primary"] {
        background: var(--primary);
        border: none;
        font-weight: 600;
    }
    .stButton button[kind="primary"]:hover {
        background: var(--secondary);
        transform: translateY(-1px);
    }

    /* Source Links */
    .source-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border-color);
        padding: 0.5rem;
        border-radius: 6px;
        margin-top: 5px;
        font-size: 0.8rem;
        color: #cbd5e1;
    }
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

def clear_database():
    vectors_path = Path("data/vectors")
    repos_path = Path("data/repos")
    if vectors_path.exists():
        shutil.rmtree(vectors_path, ignore_errors=True)
    if repos_path.exists():
        shutil.rmtree(repos_path, ignore_errors=True)
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def index_repository(repo_url, progress_callback=None):
    try:
        from src.ingestion import GitHubLoader
        from src.chunking import ASTChunker
        from src.retrieval import HybridRetriever, LightweightReranker
        from src.generation import CodeGenerator, CodeIntelligence
    except ImportError:
        st.error("Engine components not found. Ensure 'src' directory is present.")
        return None

    if progress_callback: progress_callback(10, "Cloning repository...")
    loader = GitHubLoader()
    files = loader.clone_repo(repo_url)
    
    if progress_callback: progress_callback(30, f"Parsing {len(files)} files...")
    chunker = ASTChunker()
    chunks = chunker.chunk_files(files)
    
    if progress_callback: progress_callback(50, f"Generating vectors...")
    retriever = HybridRetriever()
    generator = CodeGenerator()
    reranker = LightweightReranker()
    retriever.index(chunks, files)
    
    if progress_callback: progress_callback(90, "Finalizing engine...")
    intelligence = CodeIntelligence(retriever, generator)
    
    return {
        "files": files, "chunks": chunks, "retriever": retriever, "generator": generator,
        "reranker": reranker, "intelligence": intelligence,
        "repo_name": loader._parse_repo_name(repo_url)
    }

# -----------------------------------------------------------------------------
# SIDEBAR REFINEMENT
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 2rem;">
        <div style="background: var(--primary); padding: 6px; border-radius: 8px; color: white; display: flex;">
            {SVGS['zap'].replace('width="24"', 'width="20"').replace('height="24"', 'height="20"')}
        </div>
        <div style="font-weight: 800; font-size: 1.2rem; letter-spacing: -0.02em;">CodeLens</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("CONNECT REPOSITORY")
    repo_url = st.text_input("Repo URL", placeholder="https://github.com/...", label_visibility="collapsed")
    index_btn = st.button("Index Library", type="primary", use_container_width=True)

    if index_btn and repo_url:
        try:
            clear_database()
            bar = st.progress(0, text="Initializing...")
            def up(p, t): bar.progress(p, text=t)
            res = index_repository(repo_url, up)
            if res:
                st.session_state.update({
                    "files": res["files"], "retriever": res["retriever"], "generator": res["generator"],
                    "reranker": res["reranker"], "intelligence": res["intelligence"],
                    "repo_name": res["repo_name"], "files_count": len(res["files"]),
                    "chunks_count": len(res["chunks"]), "indexed": True, "messages": []
                })
                bar.empty()
                st.rerun()
        except Exception as e:
            st.error(f"Failed: {str(e)}")

    if st.session_state.indexed:
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("SETTINGS")
        top_k = st.slider("Context Nodes", 1, 15, 5)
        use_reranking = st.checkbox("Semantic Rerank", True)
        if st.button("Clear Session", use_container_width=True):
            clear_database()
            st.rerun()

# -----------------------------------------------------------------------------
# MAIN VIEW: LANDING
# -----------------------------------------------------------------------------
if not st.session_state.indexed:
    st.markdown(f"""
    <div class="hero-container">
        <h1 class="hero-title">Intelligent Code Navigation.</h1>
        <p class="hero-subtitle">CodeLens parses ASTs and builds semantic vectors of your repository, allowing you to query logic across file boundaries instantly.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    features = [
        {"icon": SVGS['chat'], "title": "Contextual QA", "desc": "Chat with your source code logic directly."},
        {"icon": SVGS['layers'], "title": "AST Chunking", "desc": "Aware of code structures, not just text blocks."},
        {"icon": SVGS['git'], "title": "Auto-Docs", "desc": "Generate technical documentation from logic traces."}
    ]
    for col, f in zip([c1, c2, c3], features):
        with col:
            st.markdown(f"""
            <div class="glass-card">
                <div style="color: var(--primary); margin-bottom: 1rem;">{f['icon']}</div>
                <div style="font-weight: 700; margin-bottom: 0.5rem;">{f['title']}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;">{f['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.caption("TRY THESE LIBRARIES")
    r1, r2, r3 = st.columns(3)
    for col, url in zip([r1,r2,r3], ["tiangolo/typer", "psf/requests", "pallets/flask"]):
        with col: st.code(f"https://github.com/{url}")

# -----------------------------------------------------------------------------
# MAIN VIEW: DASHBOARD
# -----------------------------------------------------------------------------
else:
    # Header
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <div style="font-size: 0.75rem; color: var(--primary); font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;">Library Loaded</div>
        <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800;">{st.session_state.repo_name}</h1>
    </div>
    <div class="hud-container">
        <div class="hud-item">
            <div class="hud-label">Source Files</div>
            <div class="hud-value">{st.session_state.files_count}</div>
        </div>
        <div class="hud-item">
            <div class="hud-label">Vector Nodes</div>
            <div class="hud-value">{st.session_state.chunks_count}</div>
        </div>
        <div class="hud-item">
            <div class="hud-label">Engine</div>
            <div class="hud-value" style="color: #10b981; font-size: 1rem;">● Operational</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_chat, tab_explain, tab_pattern, tab_docs, tab_anal = st.tabs([
        "Chat Interface", "Logic Trace", "Pattern Match", "Doc Gen", "Base Analysis"
    ])

    # --- CHAT TAB ---
    with tab_chat:
        st.markdown('<div class="chat-status-bar"><span>●</span> Knowledge base connected. Ready for queries.</div>', unsafe_allow_html=True)
        
        # History container
        message_container = st.container()
        
        # Display history
        with message_container:
            if not st.session_state.messages:
                st.markdown('<p style="color:var(--text-muted); text-align:center; padding: 2rem;">Ask anything about the repository structure or implementation.</p>', unsafe_allow_html=True)
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    if msg.get("sources"):
                        with st.expander("References"):
                            for s in msg["sources"]:
                                st.markdown(f'<div class="source-item">{SVGS["code"]} {s}</div>', unsafe_allow_html=True)

        # Input logic
        if prompt := st.chat_input("Ask about logic flow, architecture, or specific functions..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.spinner("Analyzing code context..."):
                try:
                    res = st.session_state.retriever.search(prompt, top_k=top_k*2)
                    if res and use_reranking:
                        res = st.session_state.reranker.rerank(prompt, res, top_k=top_k)
                    elif res: res = res[:top_k]
                    
                    answer = st.session_state.generator.generate(prompt, res) if res else "I couldn't find specific code context for that query."
                    sources = [f"{r['metadata'].get('file_path')} : {r['metadata'].get('name')}" for r in res] if res else []
                    
                    st.session_state.messages.append({
                        "role": "assistant", "content": answer, "sources": sources
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Analysis Error: {e}")

    # --- LOGIC EXPLAINER ---
    with tab_explain:
        col_l, col_r = st.columns(2)
        with col_l: target = st.text_input("Target Symbol", placeholder="e.g. process_data")
        with col_r: scope = st.text_input("File Scope (Optional)", placeholder="src/main.py")
        
        if st.button("Trace Logic", type="primary", use_container_width=True):
            with st.spinner("Parsing AST..."):
                try:
                    res = st.session_state.intelligence.explain_function(target, scope if scope else None)
                    if "error" in res: st.warning(res["error"])
                    else:
                        st.markdown(f"### {res['function_name']}")
                        st.markdown(f"<p style='color:var(--text-muted); font-size:0.8rem;'>{res['file_path']} : L{res.get('start_line')}</p>", unsafe_allow_html=True)
                        st.markdown(f'<div class="glass-card">{res["explanation"]}</div>', unsafe_allow_html=True)
                        with st.expander("Source Code"): st.code(res["code"], "python")
                except Exception as e: st.error(e)

    # --- PATTERN MATCH ---
    with tab_pattern:
        snippet = st.text_area("Reference Logic Snippet", placeholder="Paste code to find clones or similar logic...", height=150)
        if st.button("Identify Clones", type="primary"):
            with st.spinner("Vector scanning..."):
                res = st.session_state.intelligence.find_similar_code(snippet, 5)
                if not res: st.info("No statistically similar patterns found.")
                for r in res:
                    st.markdown(f"""
                    <div class="glass-card" style="margin-bottom:0.8rem;">
                        <div style="display:flex; justify-content:space-between;">
                            <b>{r['name']}</b>
                            <span style="color:var(--primary);">{r['similarity_score']:.2%} Match</span>
                        </div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">{r['file']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("Preview"): st.code(r["code"], "python")

    # --- DOCS ---
    with tab_docs:
        f_list = [f.path for f in st.session_state.files] if st.session_state.files else []
        sel = st.selectbox("Select Target File", f_list)
        if st.button("Generate Markdown Docs"):
            with st.spinner("Generating documentation..."):
                doc = st.session_state.intelligence.generate_documentation(sel)
                st.markdown(f'<div class="glass-card">{doc}</div>', unsafe_allow_html=True)

    # --- ANALYZE ---
    with tab_anal:
        if st.button("Run Comprehensive Scan"):
            with st.spinner("Analyzing codebase architecture..."):
                stats = st.session_state.intelligence.analyze_codebase()
                st.session_state.codebase_stats = stats
        
        if "codebase_stats" in st.session_state:
            s = st.session_state.codebase_stats
            st.markdown("#### Structural Tree")
            tree = '<div style="font-family: monospace; font-size: 0.85rem; color: var(--text-muted); background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 8px;">'
            tree += '<div style="color: var(--primary); font-weight: bold;">📦 Root</div>'
            for c in s.get("classes", [])[:10]:
                tree += f'<div style="margin-left: 20px;">├── <span style="color:#fff;">Class</span> {c["name"]}</div>'
            tree += '</div>'
            st.markdown(tree, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.caption("DETECTED CLASSES")
                for c in s.get("classes", [])[:15]:
                    st.markdown(f'<div class="source-item">{c["name"]}</div>', unsafe_allow_html=True)
            with c2:
                st.caption("DETECTED FUNCTIONS")
                for f in s.get("functions", [])[:15]:
                    st.markdown(f'<div class="source-item">{f["name"]}</div>', unsafe_allow_html=True)
