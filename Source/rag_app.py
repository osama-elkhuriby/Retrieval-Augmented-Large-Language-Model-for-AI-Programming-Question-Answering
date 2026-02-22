import streamlit as st
import requests

API_BASE = "http://localhost:5000/api/v1"

# ---------- helpers ----------
def get_project_id():
    try:
        r = requests.get(f"{API_BASE}/data/projects", timeout=5)
        if r.status_code == 200:
            data = r.json()
            projects = data.get("projects", [])
            if projects:
                return projects[0].get("project_id", "1")
    except:
        pass
    return "1"

def ask_backend(question):
    project_id = get_project_id()
    try:
        r = requests.post(
            f"{API_BASE}/nlp/index/answer/{project_id}",
            json={"text": question, "limit": 2},
            timeout=None
        )
        if r.status_code == 200:
            return r.json().get("answer", "No answer returned")
        else:
            return f"⚠️ Error: {r.text}"
    except Exception as e:
        return f"⚠️ Cannot reach backend: {e}"

# ---------- PAGE ----------
st.set_page_config(page_title="AI Programming Assistant", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 850px;
}

.chat-title {
    text-align:center;
    font-size:28px;
    font-weight:800;
    margin-bottom:5px;
}

.chat-sub {
    text-align:center;
    color:gray;
    margin-bottom:25px;
}

.footer {
    text-align:center;
    color:gray;
    margin-top:40px;
    font-size:13px;
}
.footer strong{
    color:#6C63FF;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="chat-title">🤖 AI Programming Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-sub">Powered by RAG · Ollama · Qdrant</div>', unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("📘 Project Info")
    st.markdown("""
    **Tech Stack**
    - RAG pipeline  
    - Ollama LLM  
    - Qdrant Vector DB  
    - FastAPI backend  
    """)

# ---------- CHAT HISTORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- INPUT ----------
if prompt := st.chat_input("Ask about Python, ML, PyTorch, TensorFlow..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_backend(prompt)
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
<strong>CSAI-810 | Team 35 </strong><br>
Osama Elkhuribi & Esraa Nematalla
</div>
""", unsafe_allow_html=True)