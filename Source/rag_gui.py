import streamlit as st
import requests
import time

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
API_BASE    = "http://localhost:5000/api/v1"
PROJECT_ID  = "csai810"   # fixed project, no user input needed

st.set_page_config(
    page_title="AI Docs Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* ── Background ── */
.stApp {
    background: linear-gradient(160deg, #0f172a 0%, #1e293b 60%, #0f172a 100%);
    min-height: 100vh;
}

/* ── All text visible ── */
h1,h2,h3,h4,h5,h6,p,span,label,div,li,td,th,caption {
    color: #f1f5f9 !important;
}
.stMarkdown p { color: #cbd5e1 !important; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.4);
    color: #a5b4fc !important;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    color: #f8fafc !important;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}
.hero-title span { color: #818cf8 !important; }
.hero-sub {
    font-size: 0.92rem;
    color: #94a3b8 !important;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Status pill ── */
.status-online  { color: #4ade80 !important; font-size:0.78rem; font-weight:700; }
.status-offline { color: #f87171 !important; font-size:0.78rem; font-weight:700; }

/* ── Cards ── */
.card {
    background: rgba(30,41,59,0.8);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}
.card-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: #818cf8 !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.8rem;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.6);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(99,102,241,0.15);
    margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #64748b !important;
    padding: 0.5rem 1.2rem !important;
    background: transparent !important;
    border: none !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,0.25) !important;
    color: #a5b4fc !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: rgba(15,23,42,0.8) !important;
    color: #f1f5f9 !important;
    border: 1.5px solid rgba(99,102,241,0.3) !important;
    border-radius: 10px !important;
    font-size: 0.92rem !important;
    caret-color: #818cf8;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #475569 !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
.stTextInput label, .stTextArea label {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(15,23,42,0.6) !important;
    border: 2px dashed rgba(99,102,241,0.35) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] * { color: #94a3b8 !important; }
[data-testid="stFileUploader"] small { color: #64748b !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.45) !important;
}

/* ── Slider ── */
.stSlider label { color: #94a3b8 !important; font-size:0.82rem !important; font-weight:600 !important; }
[data-testid="stSlider"] [role="slider"] { background: #6366f1 !important; }

/* ── Checkbox ── */
[data-testid="stCheckbox"] p { color: #94a3b8 !important; font-size:0.85rem !important; }

/* ── Answer box ── */
.answer-box {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.3);
    border-left: 4px solid #6366f1;
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    font-size: 0.95rem;
    line-height: 1.9;
    color: #e2e8f0 !important;
    margin-top: 0.8rem;
}

/* ── Result card ── */
.result-card {
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
    font-size: 0.87rem;
    line-height: 1.75;
    color: #cbd5e1 !important;
}
.result-num {
    font-size: 0.68rem;
    font-weight: 700;
    color: #818cf8 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
}

/* ── Alerts ── */
.stSuccess > div { background: rgba(74,222,128,0.1) !important; border-color: rgba(74,222,128,0.3) !important; }
.stSuccess p     { color: #4ade80 !important; }
.stError > div   { background: rgba(248,113,113,0.1) !important; border-color: rgba(248,113,113,0.3) !important; }
.stError p       { color: #f87171 !important; }
.stWarning > div { background: rgba(251,191,36,0.1) !important; border-color: rgba(251,191,36,0.3) !important; }
.stWarning p     { color: #fbbf24 !important; }
.stInfo > div    { background: rgba(99,102,241,0.1) !important; border-color: rgba(99,102,241,0.3) !important; }
.stInfo p        { color: #a5b4fc !important; }

/* ── Caption ── */
.stCaption p, [data-testid="stCaptionContainer"] p { color: #64748b !important; font-size:0.8rem !important; }

/* ── Expander ── */
details { background: rgba(15,23,42,0.5) !important; border: 1px solid rgba(99,102,241,0.2) !important; border-radius: 10px !important; }
summary p { color: #94a3b8 !important; font-weight: 600 !important; }

/* ── Code block ── */
.stCodeBlock { background: rgba(0,0,0,0.4) !important; border-radius: 10px !important; }

/* ── Divider ── */
hr { border-color: rgba(99,102,241,0.15) !important; }

/* ── Chip row ── */
.chip {
    display: inline-block;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    color: #a5b4fc !important;
    border-radius: 20px;
    padding: 3px 11px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 2px;
}

/* ── Footer ── */
.footer {
    text-align: center;
    margin-top: 3rem;
    padding: 1.5rem 0 1rem;
    border-top: 1px solid rgba(99,102,241,0.15);
}
.footer-project { font-size: 0.78rem; font-weight: 700; color: #818cf8 !important; letter-spacing: 1px; }
.footer-names   { font-size: 0.85rem; color: #94a3b8 !important; margin-top: 4px; }
.footer-tech    { font-size: 0.72rem; color: #475569 !important; margin-top: 6px; }

/* ── Step badge ── */
.step-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px; height: 26px;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    color: #a5b4fc !important;
    border-radius: 50%;
    font-size: 0.75rem;
    font-weight: 700;
    margin-right: 8px;
}
.step-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #e2e8f0 !important;
    display: flex;
    align-items: center;
    margin-bottom: 0.6rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────────
def api_post(path, json_data=None, files=None, timeout=None):
    try:
        r = requests.post(f"{API_BASE}{path}", json=json_data, files=files, timeout=timeout)
        return r.json(), r.status_code
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot reach the server. Is the backend running on port 5000?"}, 0
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}, 0
    except Exception as e:
        return {"error": str(e)}, 0

def api_get(path, timeout=15):
    try:
        r = requests.get(f"{API_BASE}{path}", timeout=timeout)
        return r.json(), r.status_code
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot reach the server."}, 0
    except Exception as e:
        return {"error": str(e)}, 0

def is_online():
    try:
        requests.get(API_BASE.replace("/api/v1", ""), timeout=3)
        return True
    except:
        return False


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
online = is_online()
status_html = (
    '<span class="status-online">● Connected</span>'
    if online else
    '<span class="status-offline">● Backend Offline</span>'
)

st.markdown(f"""
<div class="hero">
    <div class="hero-badge">RAG · AI Programming Assistant</div>
    <div class="hero-title">Ask anything about<br><span>AI & Programming</span></div>
    <div class="hero-sub">
        Powered by your own documents — Python, PyTorch, TensorFlow, ML concepts and more.
    </div>
    <div style="margin-top:1rem">{status_html}</div>
</div>
""", unsafe_allow_html=True)

# Topics chips
st.markdown("""
<div style="text-align:center;margin-bottom:1.5rem;">
    <span class="chip">🐍 Python</span>
    <span class="chip">🔥 PyTorch</span>
    <span class="chip">📐 TensorFlow</span>
    <span class="chip">🧠 ML Concepts</span>
    <span class="chip">📚 RAG</span>
</div>
""", unsafe_allow_html=True)

if not online:
    st.error("⚠️ Backend is not running. Start it with:\n```bash\nuvicorn main:app --host 0.0.0.0 --port 5000 --reload\n```")
    st.stop()

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["💬  Ask AI", "📁  Add Documents", "🔎  Search"])


# ════════════════════════════════════════════
# TAB 1 — ASK AI  (default / main tab)
# ════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="step-title">
        Ask a question about AI & Programming
    </div>
    <p style="color:#64748b;font-size:0.83rem;margin-bottom:1rem;">
        The assistant searches through indexed documents and generates a grounded answer.
    </p>
    """, unsafe_allow_html=True)

    question = st.text_area(
        "question",
        placeholder="e.g. How do I define a custom dataset in PyTorch?",
        height=110,
        label_visibility="collapsed"
    )
    chunks = st.slider("Context chunks to retrieve", 1, 15, 5)

    if st.button("🤖  Get Answer"):
        if not question.strip():
            st.warning("Please type a question first.")
        else:
            with st.spinner("Searching documents and generating answer..."):
                resp, code = api_post(
                    f"/nlp/index/answer/{PROJECT_ID}",
                    json_data={"text": question, "limit": chunks}
                )
            if code == 200:
                answer = resp.get("answer", "No answer returned.")
                st.markdown(f'<div class="answer-box">🤖 {answer}</div>', unsafe_allow_html=True)
                with st.expander("📄 View retrieved context"):
                    st.code(resp.get("full_prompt", ""), language="markdown")
            else:
                st.error(resp.get("error") or resp.get("signal") or "Something went wrong")

    # Example questions
    st.divider()
    st.markdown('<p style="color:#475569;font-size:0.78rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;">Try an example</p>', unsafe_allow_html=True)
    examples = [
        "How do I define a custom Dataset in PyTorch?",
        "What is the difference between a CNN and RNN?",
        "How do I use TensorFlow to build a simple neural network?",
        "What is backpropagation and how does it work?",
    ]
    c1, c2 = st.columns(2)
    for i, ex in enumerate(examples):
        with (c1 if i % 2 == 0 else c2):
            if st.button(f"› {ex}", key=f"ex{i}", use_container_width=True):
                st.info(f'📋 Copy into the box above:\n**"{ex}"**')


# ════════════════════════════════════════════
# TAB 2 — ADD DOCUMENTS
# ════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="step-title">Add new documents to the knowledge base</div>
    <p style="color:#64748b;font-size:0.83rem;margin-bottom:1.2rem;">
        Upload a PDF or text file, then index it so the AI can answer questions from it.
    </p>
    """, unsafe_allow_html=True)

    # ── Step 1: Upload ──
    st.markdown('<div class="step-title"><span class="step-badge">1</span> Upload a document</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("file", type=["pdf", "txt", "md"], label_visibility="collapsed")

    asset_name = None  # will hold the asset_name (file_id) returned from upload

    if uploaded:
        st.caption(f"📄 {uploaded.name} · {uploaded.size / 1024:.1f} KB")
        if st.button("⬆️  Upload", key="upload"):
            with st.spinner("Uploading..."):
                files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
                resp, code = api_post(f"/data/upload/{PROJECT_ID}", files=files)
            if code == 200:
                # upload returns file_id = asset_name (UUID filename) stored in DB
                # process route uses asset_name to look up the record via get_asset_record()
                asset_name = resp.get("file_id", "")
                st.success(f"✅ Uploaded successfully!")
                st.session_state["uploaded_asset_name"] = asset_name
                st.session_state["upload_done"] = True
            else:
                st.error(resp.get("error") or resp.get("signal") or "Upload failed")

    st.divider()

    # ── Step 2: Process ──
    st.markdown('<div class="step-title"><span class="step-badge">2</span> Process into chunks</div>', unsafe_allow_html=True)
    st.caption("Splits the document into pieces the AI can read and index")

    col_a, col_b = st.columns(2)
    with col_a:
        chunk_size = st.slider("Chunk size", 64, 1024, 512, 64)
    with col_b:
        overlap = st.slider("Overlap", 0, 256, 64, 16)

    # asset_name is what the process route expects — it matches asset_name in MongoDB
    stored_asset_name = st.session_state.get("uploaded_asset_name", "")
    if stored_asset_name:
        st.caption(f"📄 Ready to process: `{stored_asset_name}`")
    else:
        st.caption("Upload a file first, or leave blank to process all files in the project")
    reset_chunks = st.checkbox("Reset chunks before processing")

    if st.button("⚙️  Process", key="process"):
        with st.spinner("Processing..."):
            payload = {
                "chunk_size": chunk_size,
                "overlap_size": overlap,
                "do_reset": 1 if reset_chunks else 0,
            }
            # send asset_name as file_id — the route calls get_asset_record(asset_name=file_id)
            if stored_asset_name:
                payload["file_id"] = stored_asset_name
            resp, code = api_post(f"/data/process/{PROJECT_ID}", json_data=payload)
        if code == 200:
            st.success(f"✅ {resp.get('inserted_chunks', 0)} chunks from {resp.get('processed_files', 0)} file(s)")
            st.session_state["process_done"] = True
        else:
            st.error(resp.get("error") or resp.get("signal") or "Processing failed")

    st.divider()

    # ── Step 3: Index ──
    st.markdown('<div class="step-title"><span class="step-badge">3</span> Index into Vector Database</div>', unsafe_allow_html=True)
    st.caption("Embeds the chunks using Ollama and stores them in Qdrant for semantic search")
    reset_idx = st.checkbox("Reset vector DB before indexing")

    if st.button("🚀  Index Now", key="index"):
        with st.spinner("Embedding and indexing — this may take a moment..."):
            resp, code = api_post(
                f"/nlp/index/push/{PROJECT_ID}",
                json_data={"do_reset": 1 if reset_idx else 0}
            )
        if code == 200:
            st.success(f"✅ {resp.get('inserted_items_count', 0)} chunks indexed! You can now ask questions.")
            st.session_state.pop("uploaded_asset_name", None)
            st.session_state.pop("upload_done", None)
            st.session_state.pop("process_done", None)
        else:
            st.error(resp.get("error") or resp.get("signal") or "Indexing failed")


# ════════════════════════════════════════════
# TAB 3 — SEARCH
# ════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class="step-title">Semantic Search</div>
    <p style="color:#64748b;font-size:0.83rem;margin-bottom:1.2rem;">
        Find relevant document chunks directly without AI generation.
    </p>
    """, unsafe_allow_html=True)

    query = st.text_input("search", placeholder="e.g. gradient descent learning rate...", label_visibility="collapsed")
    limit = st.slider("Results", 1, 20, 5)

    if st.button("🔎  Search", key="search"):
        if not query.strip():
            st.warning("Please enter a search term.")
        else:
            with st.spinner("Searching..."):
                resp, code = api_post(
                    f"/nlp/index/search/{PROJECT_ID}",
                    json_data={"text": query, "limit": limit}
                )
            if code == 200:
                results = resp.get("results", [])
                st.caption(f"Found **{len(results)}** result(s)")
                for i, r in enumerate(results):
                    score     = r.get("score", r.get("similarity", "—"))
                    text      = r.get("text", r.get("chunk_text", str(r)))
                    score_str = f"{score:.4f}" if isinstance(score, float) else str(score)
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-num">Result {i+1} · Score: {score_str}</div>
                        {text}
                    </div>""", unsafe_allow_html=True)
            else:
                st.error(resp.get("error") or resp.get("signal") or "Search failed")


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-project">CSAI-810 Project · Team 35</div>
    <div class="footer-names">Osama Elkhuribi &amp; Esraa Nematalla</div>
    <div class="footer-tech">Ollama · Qdrant · FastAPI · Streamlit</div>
</div>
""", unsafe_allow_html=True)
