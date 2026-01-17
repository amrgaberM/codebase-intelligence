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
    "search": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>""",
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
    /* Global Variables & Reset */
    :root {
        --primary: #6366f1;
        --secondary: #8b5cf6;
        --accent: #06b6d4;
        --bg-dark: #0f1117;
        --bg-card: rgba(20, 25, 40, 0.7);
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --border: rgba(99, 102, 241, 0.15);
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* App Background */
    .stApp {
        background: linear-gradient(-45deg, #0f1117, #1e1b4b, #0f0f15, #111827);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: var(--text-primary);
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99, 102, 241, 0.4); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--primary); }

    /* Typography */
    h1, h2, h3, h4, h5, h6 { font-family: 'Inter', sans-serif; letter-spacing: -0.01em; }
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 5rem 2rem;
        background: radial-gradient(circle at center, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
        border-radius: 30px;
        margin-bottom: 3rem;
        border: 1px solid var(--border);
        box-shadow: 0 0 80px -20px rgba(99, 102, 241, 0.15);
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 20%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        text-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        max-width: 650px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Cards */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
    }

    /* Icon Box */
    .icon-box {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(6, 182, 212, 0.15));
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    .icon-box svg { width: 26px; height: 26px; }

    /* HUD Stats */
    .hud-container {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .hud-item {
        flex: 1;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid var(--border);
        padding: 1.25rem;
        border-radius: 12px;
        min-width: 160px;
        position: relative;
        overflow: hidden;
    }
    .hud-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--primary);
    }
    .hud-item:last-child::before { background: var(--accent); }

    .hud-value { font-size: 1.75rem; font-weight: 700; color: #fff; margin-bottom: 0.25rem; }
    .hud-label { font-size: 0.7rem; text-transform: uppercase; color: var(--text-secondary); letter-spacing: 0.1em; }

    /* Timeline Steps */
    .step-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px dashed var(--border);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        position: relative;
        transition: 0.3s;
    }
    .step-card:hover { background: rgba(15, 23, 42, 0.8); border-style: solid; }
    .step-badge {
        position: absolute;
        top: -14px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        color: white;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 100px;
        font-size: 0.85rem;
        box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
    }

    /* Fixed Chat History Container */
    .chat-history-container {
        height: calc(100vh - 350px);
        overflow-y: auto;
        padding-right: 15px;
        padding-bottom: 20px;
        padding-top: 10px;
        scrollbar-width: thin;
    }
    
    .chat-status-bar {
        font-size: 0.8rem;
        color: var(--text-secondary);
        background: rgba(99, 102, 241, 0.1);
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid var(--border);
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Tree View CSS */
    .tree-view {
        font-family: 'JetBrains Mono', monospace;
        color: #e2e8f0;
        padding: 1rem;
    }
    .tree-node {
        margin-left: 1.5rem;
        position: relative;
        padding-left: 0.5rem;
        border-left: 1px dashed var(--primary);
        line-height: 2;
    }
    .tree-node::before {
        content: '';
        position: absolute;
        top: 14px;
        left: 0;
        width: 10px;
        height: 1px;
        background: var(--primary);
    }
    .tree-root { font-weight: bold; color: var(--accent); margin-bottom: 0.5rem; }
    .tree-leaf { color: #94a3b8; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #080a0f;
        border-right: 1px solid var(--border);
    }
    
    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
        background-color: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.15) !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
        transition: 0.2s;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
        background-color: rgba(30, 41, 59, 0.9) !important;
    }

    /* Buttons */
    .stButton button {
        border-radius: 10px;
        font-weight: 600;
        letter-spacing: 0.02em;
        transition: all 0.25s;
        border: none;
    }
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
    }
    .stButton button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border);
        color: var(--text-secondary);
    }
    .stButton button:hover {
        transform: translateY(-2px);
        filter: brightness(1.1);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(15, 23, 42, 0.5);
        padding: 5px;
        border-radius: 12px;
        border: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: transparent;
        border: none;
        color: var(--text-secondary);
        font-weight: 500;
        border-radius: 8px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(99, 102, 241, 0.2);
        color: #fff;
    }

    /* Source Item */
    .source-item {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 8px;
        padding: 0.85rem;
        margin-bottom: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #cbd5e1;
    }
    .source-item svg { width: 14px; height: 14px; opacity: 0.7; }
    
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
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <div style="width: 32px; height: 32px; background: #6366f1; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white;">
            {SVGS['zap'].replace('width="24"', 'width="18"').replace('height="24"', 'height="18"')}
        </div>
        <h2 style="margin: 0; font-size: 1.4rem; font-weight: 700; color: #fff;">CodeLens</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("REPOSITORY CONTROL")
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
    
    # Display Estimate in Sidebar
    if st.session_state.get("show_estimate", False) and "estimate_data" in st.session_state:
        est = st.session_state.estimate_data
        st.markdown(f"""
        <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px; padding: 12px; margin: 10px 0;">
            <div style="color: #a5b4fc; font-weight: bold; font-size: 1.1rem;">{est['est_time_str']}</div>
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
                    status_box.caption(f"{text}")
                
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
        if st.button("Reset Session", type="secondary", use_container_width=True):
            clear_database()
            st.rerun()
            
        st.divider()
        st.caption("ADVANCED SETTINGS")
        top_k = st.slider("Context Window", 1, 10, 5)
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
        <p class="hero-subtitle">Turn your repository into an intelligent knowledge base.<br>
        Ask questions, trace dependencies, and generate documentation instantly.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Grid
    c1, c2, c3, c4 = st.columns(4)
    
    features = [
        {"icon": SVGS['chat'], "title": "Natural QA", "desc": "Context-aware chat interactions."},
        {"icon": SVGS['search'], "title": "Deep Search", "desc": "Semantic & keyword retrieval."},
        {"icon": SVGS['git'], "title": "Dependency", "desc": "Cross-file logic tracing."},
        {"icon": SVGS['layers'], "title": "AST Parsing", "desc": "Structure-aware chunking."}
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
    st.markdown('<h2 style="text-align: center; margin: 5rem 0 3rem;">Workflow</h2>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    
    steps = [
        {"num": "1", "title": "Connect", "desc": "Paste a GitHub URL to start cloning."},
        {"num": "2", "title": "Analyze", "desc": "AI processes syntax trees and vectors."},
        {"num": "3", "title": "Explore", "desc": "Interact with your codebase via chat."}
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

    # Suggested Repos (Fixed URLs)
    st.markdown('<div style="margin-top: 5rem;"></div>', unsafe_allow_html=True)
    st.caption("POPULAR REPOSITORIES")
    r1, r2, r3 = st.columns(3)
    
    repos = [
        {"name": "tiangolo/typer", "type": "CLI Framework"},
        {"name": "psf/requests", "type": "HTTP Library"},
        {"name": "pallets/flask", "type": "Web Framework"}
    ]
    
    for col, repo in zip([r1, r2, r3], repos):
        with col:
            st.code(f"https://github.com/{repo['name']}")

# --- VIEW: DASHBOARD (INDEXED) ---
else:
    # Header & HUD
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.5rem;">
        <div>
            <h1 style="margin: 0; background: linear-gradient(to right, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{st.session_state.get("repo_name", "Repository")}</h1>
            <p style="color: #64748b; margin: 0; font-size: 0.9rem;">Interactive Intelligence Dashboard</p>
        </div>
    </div>
    
    <div class="hud-container">
        <div class="hud-item">
            <div class="hud-value">{st.session_state.get("files_count", 0)}</div>
            <div class="hud-label">Source Files</div>
        </div>
        <div class="hud-item">
            <div class="hud-value">{st.session_state.get("chunks_count", 0)}</div>
            <div class="hud-label">Vector Chunks</div>
        </div>
        <div class="hud-item" style="border-left-color: var(--accent);">
            <div class="hud-value">Active</div>
            <div class="hud-label">Engine Status</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Chat & Query", "Logic Explainer", "Pattern Match", "Auto Docs", "Deep Analysis"])
    
    # --- TAB 1: CHAT ---
    with tab1:
        # Fixed height container for chat history
        chat_container = st.container()
        
        with chat_container:
            st.markdown('<div class="chat-status-bar">🟢 Connected to Knowledge Base</div>', unsafe_allow_html=True)
            st.markdown('<div class="chat-history-container">', unsafe_allow_html=True)
            
            # Show empty state if no messages
            if not st.session_state.get("messages", []):
                st.markdown("""
                <div style="text-align: center; color: #64748b; padding: 2rem;">
                    <p>👋 Ask anything about your codebase structure or logic.</p>
                </div>
                """, unsafe_allow_html=True)

            for msg in st.session_state.get("messages", []):
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    if msg.get("sources"):
                        with st.expander("References"):
                            for src in msg["sources"]:
                                st.markdown(f'<div class="source-item">{SVGS["code"]} {src}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Input (Automatically fixed at bottom by Streamlit)
        if prompt := st.chat_input("Ask about logic, patterns, or architecture..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun() # Rerun to show user message immediately inside container

        # Handle Response generation after rerun
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
             with st.spinner("Processing..."):
                try:
                    start = time.time()
                    retriever = st.session_state.get("retriever")
                    generator = st.session_state.get("generator")
                    reranker = st.session_state.get("reranker")
                    
                    last_msg = st.session_state.messages[-1]["content"]
                    results = retriever.search(last_msg, top_k=top_k*2)
                    
                    if results and use_reranking:
                        results = reranker.rerank(last_msg, results, top_k=top_k)
                    elif results:
                        results = results[:top_k]
                    
                    if results:
                        answer = generator.generate(last_msg, results)
                    else:
                        answer = "No relevant code segments found in the index."
                    
                    elapsed = time.time() - start
                except Exception as e:
                    answer = f"Error: {str(e)}"
                    results = []
                    elapsed = 0
            
                sources = []
                if results:
                    for i, r in enumerate(results[:5], 1):
                        meta = r.get("metadata", {})
                        src_text = f"{meta.get('file_path', '?')} : {meta.get('name', '?')}"
                        sources.append(src_text)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
                st.rerun()

    # --- TAB 2: EXPLAIN ---
    with tab2:
        col_ex1, col_ex2 = st.columns([1, 1])
        with col_ex1:
            func_name = st.text_input("Target Function/Class", placeholder="e.g. process_request")
        with col_ex2:
            file_path = st.text_input("File Scope (Optional)", placeholder="src/main.py")
            
        if st.button("Analyze Logic", type="primary", use_container_width=True):
            if func_name:
                with st.spinner("Tracing AST..."):
                    try:
                        intelligence = st.session_state.get("intelligence")
                        result = intelligence.explain_function(func_name, file_path if file_path else None)
                        
                        if "error" in result:
                            st.warning(result["error"])
                        else:
                            st.markdown(f"### {result['function_name']}")
                            st.caption(f"Location: {result['file_path']} : Lines {result.get('start_line', '?')}-{result.get('end_line', '?')}")
                            
                            st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
                            st.markdown(result["explanation"])
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            with st.expander("Source Code"):
                                st.code(result["code"], language="python")
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")

    # --- TAB 3: SIMILAR ---
    with tab3:
        code_snippet = st.text_area("Reference Logic", placeholder="Paste code snippet to find similar patterns...", height=200)
        
        if st.button("Identify Patterns", type="primary"):
            if code_snippet:
                with st.spinner("Comparing vectors..."):
                    try:
                        intelligence = st.session_state.get("intelligence")
                        results = intelligence.find_similar_code(code_snippet, top_k=5)
                        
                        if results:
                            for i, r in enumerate(results, 1):
                                st.markdown(f"""
                                <div class="glass-card" style="margin-bottom: 1rem;">
                                    <div style="display: flex; justify-content: space-between;">
                                        <h4 style="margin:0; font-size: 1rem;">{r['name']}</h4>
                                        <span style="color: var(--accent); font-weight: bold;">{r['similarity_score']:.2f} Match</span>
                                    </div>
                                    <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 5px;">{r['file']} | Line {r['line']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                with st.expander(f"Code Preview"):
                                    st.code(r["code"], language="python")
                        else:
                            st.info("No statistically similar patterns found.")
                    except Exception as e:
                        st.error(str(e))

    # --- TAB 4: DOCS ---
    with tab4:
        files = st.session_state.get("files", [])
        file_paths = [f.path for f in files] if files else []
        
        selected_file = st.selectbox("Target File", file_paths if file_paths else ["Index empty"])
        
        if st.button("Generate Docs", key="docs_btn"):
            if selected_file and selected_file != "Index empty":
                with st.spinner("Writing documentation..."):
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
            if st.button("Run Global Analysis", use_container_width=True):
                with st.spinner("Scanning structure..."):
                    try:
                        intelligence = st.session_state.get("intelligence")
                        stats = intelligence.analyze_codebase()
                        st.session_state.codebase_stats = stats
                    except Exception as e:
                        st.error(str(e))
        with c2:
            if st.button("Trace Symbol Usage", use_container_width=True):
                st.session_state.show_usage_input = True

        if "codebase_stats" in st.session_state:
            stats = st.session_state.codebase_stats
            
            # CSS Tree Visualization instead of Graphviz
            st.subheader("Structure Map")
            
            tree_html = '<div class="tree-view">'
            tree_html += '<div class="tree-root">📦 Root</div>'
            
            # Simple visualization of top files/classes
            for cls in stats.get("classes", [])[:8]:
                tree_html += f'<div class="tree-node"><span class="tree-leaf">Class:</span> {cls["name"]} <span style="opacity:0.5; font-size:0.8em">({cls["file"]})</span></div>'
            for func in stats.get("functions", [])[:5]:
                tree_html += f'<div class="tree-node"><span class="tree-leaf">Func:</span> {func["name"]} <span style="opacity:0.5; font-size:0.8em">({func["file"]})</span></div>'
            
            tree_html += '</div>'
            
            st.markdown(f"""
            <div class="glass-card">
                {tree_html}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            d1, d2 = st.columns(2)
            with d1:
                st.markdown("##### Detected Classes")
                for cls in stats.get("classes", [])[:10]:
                    st.markdown(f'<div class="source-item">{SVGS["box"]} {cls["name"]} <span style="color: #64748b; margin-left: auto;">{cls["file"]}</span></div>', unsafe_allow_html=True)
            with d2:
                st.markdown("##### Detected Functions")
                for func in stats.get("functions", [])[:10]:
                    st.markdown(f'<div class="source-item">{SVGS["code"]} {func["name"]} <span style="color: #64748b; margin-left: auto;">{func["file"]}</span></div>', unsafe_allow_html=True)

        if st.session_state.get("show_usage_input", False):
            st.divider()
            usage_name = st.text_input("Enter symbol name", key="usage_input", placeholder="e.g. BaseLoader")
            if st.button("Trace"):
                with st.spinner("Mapping references..."):
                    try:
                        intelligence = st.session_state.get("intelligence")
                        usages = intelligence.find_usages(usage_name)
                        st.success(f"Found {usages['total_usages']} references")
                        
                        udata = usages.get("usages", {})
                        if udata.get("definition"):
                            d = udata["definition"]
                            st.markdown(f"**Definition:** `{d['file']}:{d['line']}`")
                        
                        if udata.get("calls"):
                            st.markdown("**Call Sites:**")
                            for call in udata["calls"][:10]:
                                st.markdown(f"- `{call['file']}` at line {call['line']}")
                    except Exception as e:
                        st.error(str(e))
