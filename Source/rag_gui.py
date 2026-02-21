import streamlit as st
import requests
import json

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
API_BASE = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="RAG Studio",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* Reset & base */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
}

/* App background */
.stApp {
    background: #0a0a0f;
    color: #e8e4d9;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f18 !important;
    border-right: 1px solid #1e1e2e;
}
[data-testid="stSidebar"] * {
    color: #e8e4d9 !important;
}

/* Header */
.rag-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 2rem 0 1rem;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 2rem;
}
.rag-logo {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #c8f542;
    letter-spacing: -2px;
    line-height: 1;
}
.rag-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #555570;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* Cards */
.metric-card {
    background: #0f0f18;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1.4rem;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #c8f542; }
.metric-label {
    font-size: 0.65rem;
    color: #555570;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #c8f542;
}

/* Buttons */
.stButton > button {
    background: #c8f542 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    letter-spacing: 1px !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #d9ff5a !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(200, 245, 66, 0.3) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: #0f0f18 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 8px !important;
    color: #e8e4d9 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #c8f542 !important;
    box-shadow: 0 0 0 2px rgba(200, 245, 66, 0.15) !important;
}

/* Select */
.stSelectbox > div > div {
    background: #0f0f18 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 8px !important;
    color: #e8e4d9 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #0f0f18;
    border: 1px dashed #2a2a3e;
    border-radius: 12px;
    padding: 1rem;
}
[data-testid="stFileUploader"]:hover {
    border-color: #c8f542;
}

/* Answer box */
.answer-box {
    background: #0f0f18;
    border: 1px solid #c8f542;
    border-left: 4px solid #c8f542;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    font-size: 0.9rem;
    line-height: 1.8;
    color: #e8e4d9;
    margin-top: 1rem;
}

/* Search result card */
.result-card {
    background: #0f0f18;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    font-size: 0.82rem;
    line-height: 1.7;
    color: #b0acb0;
    transition: border-color 0.2s;
}
.result-card:hover { border-color: #333350; }
.result-score {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    color: #c8f542;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

/* Section titles */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8e4d9;
    letter-spacing: -0.5px;
    margin-bottom: 1rem;
}

/* Status pills */
.pill-success {
    display: inline-block;
    background: rgba(200,245,66,0.12);
    color: #c8f542;
    border: 1px solid rgba(200,245,66,0.3);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.7rem;
    letter-spacing: 1px;
}
.pill-error {
    display: inline-block;
    background: rgba(255,80,80,0.1);
    color: #ff6060;
    border: 1px solid rgba(255,80,80,0.3);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.7rem;
    letter-spacing: 1px;
}

/* Divider */
hr { border-color: #1e1e2e !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1e1e2e;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #555570 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
    border: none !important;
    padding: 0.6rem 1.2rem !important;
}
.stTabs [aria-selected="true"] {
    color: #c8f542 !important;
    border-bottom: 2px solid #c8f542 !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #0f0f18 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 8px !important;
    color: #e8e4d9 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a3e; border-radius: 4px; }

/* Labels */
label, .stSlider label {
    color: #888898 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.5px !important;
}

/* Radio */
.stRadio > div { gap: 8px; }
.stRadio [data-testid="stMarkdownContainer"] p {
    color: #e8e4d9 !important;
    font-size: 0.82rem !important;
}

/* Slider */
.stSlider [data-testid="stThumbValue"] { color: #c8f542 !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] { background: #c8f542 !important; }

/* Success / error messages */
.stSuccess { background: rgba(200,245,66,0.08) !important; border-color: rgba(200,245,66,0.3) !important; color: #c8f542 !important; }
.stError   { background: rgba(255,80,80,0.08) !important; border-color: rgba(255,80,80,0.3) !important; color: #ff6060 !important; }
.stWarning { background: rgba(255,180,50,0.08) !important; border-color: rgba(255,180,50,0.3) !important; color: #ffb432 !important; }
.stInfo    { background: rgba(100,160,255,0.08) !important; border-color: rgba(100,160,255,0.3) !important; color: #64a0ff !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def api_get(path):
    try:
        r = requests.get(f"{API_BASE}{path}", timeout=30)
        return r.json(), r.status_code
    except Exception as e:
        return {"error": str(e)}, 0

def api_post(path, json_data=None, files=None, timeout=120):
    try:
        r = requests.post(f"{API_BASE}{path}", json=json_data, files=files, timeout=timeout)
        return r.json(), r.status_code
    except Exception as e:
        return {"error": str(e)}, 0

def status_pill(ok, label_ok="SUCCESS", label_fail="FAILED"):
    if ok:
        return f'<span class="pill-success">✓ {label_ok}</span>'
    return f'<span class="pill-error">✗ {label_fail}</span>'


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.5rem 0 1rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#c8f542;letter-spacing:-1px;">⬡ RAG Studio</div>
        <div style="font-size:0.6rem;color:#555570;letter-spacing:3px;margin-top:4px;">POWERED BY OLLAMA</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div style="font-size:0.65rem;color:#555570;letter-spacing:2px;margin-bottom:8px;">PROJECT</div>', unsafe_allow_html=True)
    project_id = st.text_input("Project ID", value="project_1", label_visibility="collapsed", placeholder="Enter project ID...")

    st.markdown("---")
    st.markdown('<div style="font-size:0.65rem;color:#555570;letter-spacing:2px;margin-bottom:8px;">API ENDPOINT</div>', unsafe_allow_html=True)
    api_url = st.text_input("API URL", value=API_BASE, label_visibility="collapsed")

    st.markdown("---")

    # Quick health check
    if st.button("⬡  CHECK API HEALTH"):
        try:
            r = requests.get(api_url.replace("/api/v1", ""), timeout=5)
            st.markdown('<span class="pill-success">API ONLINE</span>', unsafe_allow_html=True)
        except:
            st.markdown('<span class="pill-error">API OFFLINE</span>', unsafe_allow_html=True)

    st.markdown("""
    <div style="position:fixed;bottom:1.5rem;left:1rem;right:1rem;font-size:0.6rem;color:#333350;letter-spacing:1px;">
        RAG STUDIO v0.1 · OLLAMA BACKEND
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="rag-header">
    <div>
        <div class="rag-logo">⬡ RAG Studio</div>
        <div class="rag-sub">Retrieval Augmented Generation · Project: {project_id}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  ▲  UPLOAD & INDEX  ",
    "  ◈  ASK AI  ",
    "  ◎  SEARCH  ",
    "  ⬡  PROJECT INFO  ",
])


# ══════════════════════════════════════════════
# TAB 1 — UPLOAD & INDEX
# ══════════════════════════════════════════════
with tab1:
    col_upload, col_process = st.columns([1, 1], gap="large")

    # ── Upload ──
    with col_upload:
        st.markdown('<div class="section-title">Upload Documents</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Drop your file here",
            type=["pdf", "txt", "md", "csv"],
            label_visibility="collapsed"
        )

        if uploaded_file:
            st.markdown(f"""
            <div style="background:#0f0f18;border:1px solid #1e1e2e;border-radius:8px;padding:0.8rem 1rem;margin:0.5rem 0;font-size:0.8rem;">
                <span style="color:#555570;">FILE</span>&nbsp;&nbsp;
                <span style="color:#e8e4d9;">{uploaded_file.name}</span>&nbsp;&nbsp;
                <span style="color:#c8f542;">{uploaded_file.size / 1024:.1f} KB</span>
            </div>
            """, unsafe_allow_html=True)

            if st.button("⬆  UPLOAD FILE"):
                with st.spinner("Uploading..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    resp, code = api_post(f"/data/upload/{project_id}", files=files)

                if code == 200:
                    file_id = resp.get("file_id", "")
                    st.success(f"Uploaded! File ID: `{file_id}`")
                    st.session_state["last_file_id"] = file_id
                else:
                    st.error(f"Upload failed: {resp.get('signal', resp)}")

    # ── Process ──
    with col_process:
        st.markdown('<div class="section-title">Process & Index</div>', unsafe_allow_html=True)

        chunk_size   = st.slider("Chunk Size (tokens)", 64, 1024, 512, 64)
        overlap_size = st.slider("Overlap Size (tokens)", 0, 256, 64, 16)

        file_id_input = st.text_input(
            "File ID (leave blank for all files)",
            value=st.session_state.get("last_file_id", ""),
            placeholder="Optional — processes all project files if empty"
        )

        do_reset_proc = st.checkbox("Reset existing chunks before processing")

        if st.button("⚙  PROCESS FILES"):
            with st.spinner("Processing and chunking..."):
                payload = {
                    "chunk_size": chunk_size,
                    "overlap_size": overlap_size,
                    "do_reset": 1 if do_reset_proc else 0,
                }
                if file_id_input.strip():
                    payload["file_id"] = file_id_input.strip()

                resp, code = api_post(f"/data/process/{project_id}", json_data=payload)

            if code == 200:
                st.success(f"✓ {resp.get('inserted_chunks', 0)} chunks from {resp.get('processed_files', 0)} file(s)")
            else:
                st.error(f"Processing failed: {resp.get('signal', resp)}")

    st.markdown("---")

    # ── Index to Vector DB ──
    st.markdown('<div class="section-title">Push to Vector DB</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])
    with col_a:
        do_reset_idx = st.checkbox("Reset vector collection before indexing")
    with col_b:
        push_btn = st.button("⬡  INDEX INTO VECTOR DB", use_container_width=True)

    if push_btn:
        with st.spinner("Embedding and indexing — this may take a moment..."):
            resp, code = api_post(
                f"/nlp/index/push/{project_id}",
                json_data={"do_reset": 1 if do_reset_idx else 0}
            )

        if code == 200:
            st.success(f"✓ {resp.get('inserted_items_count', 0)} chunks indexed into vector DB")
        else:
            st.error(f"Indexing failed: {resp.get('signal', resp)}")


# ══════════════════════════════════════════════
# TAB 2 — ASK AI (RAG)
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Ask your documents anything</div>', unsafe_allow_html=True)

    query_text = st.text_area(
        "Your question",
        placeholder="What does the document say about...?",
        height=100,
        label_visibility="collapsed"
    )

    col_l, col_r = st.columns([1, 2])
    with col_l:
        rag_limit = st.slider("Retrieved context chunks", 1, 20, 5)
    with col_r:
        pass

    ask_btn = st.button("◈  GET AI ANSWER", use_container_width=False)

    if ask_btn:
        if not query_text.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                resp, code = api_post(
                    f"/nlp/index/answer/{project_id}",
                    json_data={"text": query_text, "limit": rag_limit}
                )

            if code == 200:
                answer = resp.get("answer", "")
                st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

                with st.expander("▸  View full prompt sent to LLM"):
                    st.code(resp.get("full_prompt", ""), language="markdown")

                with st.expander("▸  View chat history"):
                    st.json(resp.get("chat_history", []))
            else:
                st.error(f"Error: {resp.get('signal', resp)}")

    # ── Example prompts ──
    st.markdown("---")
    st.markdown('<div style="font-size:0.65rem;color:#555570;letter-spacing:2px;margin-bottom:10px;">EXAMPLE PROMPTS</div>', unsafe_allow_html=True)
    examples = [
        "Summarize the main topics covered in the documents.",
        "What are the key conclusions or findings?",
        "List any important dates or deadlines mentioned.",
        "What recommendations are made in the document?",
    ]
    cols = st.columns(2)
    for i, ex in enumerate(examples):
        with cols[i % 2]:
            if st.button(f"› {ex}", key=f"ex_{i}", use_container_width=True):
                st.session_state["prefill_query"] = ex
                st.rerun()

    if "prefill_query" in st.session_state:
        st.info(f'Prefilled: "{st.session_state.pop("prefill_query")}" — paste it above and ask!')


# ══════════════════════════════════════════════
# TAB 3 — SEMANTIC SEARCH
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Semantic Search</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.75rem;color:#555570;margin-bottom:1.2rem;">Search the vector DB directly — returns raw matched chunks without LLM generation.</div>', unsafe_allow_html=True)

    search_text  = st.text_input("Search query", placeholder="Enter a concept, keyword, or sentence...", label_visibility="collapsed")
    search_limit = st.slider("Number of results", 1, 20, 5)

    search_btn = st.button("◎  SEARCH VECTOR DB")

    if search_btn:
        if not search_text.strip():
            st.warning("Please enter a search query.")
        else:
            with st.spinner("Searching..."):
                resp, code = api_post(
                    f"/nlp/index/search/{project_id}",
                    json_data={"text": search_text, "limit": search_limit}
                )

            if code == 200:
                results = resp.get("results", [])
                st.markdown(f'<div style="font-size:0.7rem;color:#555570;margin-bottom:1rem;">Found <span style="color:#c8f542">{len(results)}</span> results</div>', unsafe_allow_html=True)

                for i, r in enumerate(results):
                    score = r.get("score", r.get("similarity", "—"))
                    text  = r.get("text", r.get("chunk_text", str(r)))
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-score">CHUNK {i+1} &nbsp;·&nbsp; SCORE: {score if isinstance(score, str) else f"{score:.4f}"}</div>
                        {text}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error(f"Search failed: {resp.get('signal', resp)}")


# ══════════════════════════════════════════════
# TAB 4 — PROJECT INFO
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Project Overview</div>', unsafe_allow_html=True)

    col_info, col_refresh = st.columns([3, 1])
    with col_refresh:
        refresh = st.button("↻  REFRESH", use_container_width=True)

    if refresh or True:
        resp, code = api_get(f"/nlp/index/info/{project_id}")

        if code == 200:
            info = resp.get("collection_info", {})

            # Metrics row
            c1, c2, c3, c4 = st.columns(4)
            vectors_count = info.get("vectors_count", info.get("points_count", "—"))
            segments      = info.get("segments_count", "—")
            status_val    = info.get("status", "—")
            dim           = info.get("config", {}).get("params", {}).get("vectors", {}).get("size", "—")

            with c1:
                st.markdown(f'<div class="metric-card"><div class="metric-label">VECTORS</div><div class="metric-value">{vectors_count}</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-card"><div class="metric-label">SEGMENTS</div><div class="metric-value">{segments}</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-card"><div class="metric-label">DIMENSIONS</div><div class="metric-value">{dim}</div></div>', unsafe_allow_html=True)
            with c4:
                st.markdown(f'<div class="metric-card"><div class="metric-label">STATUS</div><div class="metric-value" style="font-size:1.1rem;margin-top:4px;">{status_val.upper() if isinstance(status_val, str) else status_val}</div></div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown('<div style="font-size:0.65rem;color:#555570;letter-spacing:2px;margin-bottom:10px;">RAW COLLECTION INFO</div>', unsafe_allow_html=True)
            st.json(info)
        else:
            st.error(f"Could not fetch project info: {resp.get('signal', resp)}")
            st.markdown('<div style="font-size:0.8rem;color:#555570;margin-top:0.5rem;">Make sure the project has been indexed first.</div>', unsafe_allow_html=True)
