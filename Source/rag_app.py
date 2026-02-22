"""
RAG Chat UI — runs on http://localhost:8080
Install: pip install flask flask-cors
Run:     python rag_app.py
"""

from flask import Flask, request, jsonify, Response
import requests as req
import json

API_BASE   = "http://localhost:5000/api/v1"
PROJECT_ID = "csai810"

app = Flask(__name__)

# ── Proxy to FastAPI backend ──────────────────
@app.route("/ask", methods=["POST"])
def ask():
    body = request.json
    question    = (body.get("question") or "").strip()
    num_sources = int(body.get("num_sources", 5))

    if not question:
        return jsonify({"error": "Empty question"}), 400

    try:
        r = req.post(
            f"{API_BASE}/nlp/index/answer/{PROJECT_ID}",
            json={"text": question, "limit": num_sources},
            timeout=None,
        )
        data = r.json()
        if r.status_code == 200:
            return jsonify({"answer": data.get("answer", "No answer returned.")})
        else:
            return jsonify({"error": data.get("signal") or data.get("error") or f"HTTP {r.status_code}"}), 500
    except req.exceptions.ConnectionError:
        return jsonify({"error": "Cannot reach the backend on port 5000."}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    try:
        req.get(API_BASE.replace("/api/v1", ""), timeout=3)
        return jsonify({"online": True})
    except:
        return jsonify({"online": False})


# ── Main page ─────────────────────────────────
@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")


# ── HTML ──────────────────────────────────────
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>AI Programming Assistant</title>


<style>
  /* ── Reset ── */
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: #f0f2ff;
    color: #111827;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* ── Top bar ── */
  header {
    background: #ffffff;
    border-bottom: 1px solid #e2e6f8;
    padding: 0 2rem;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
    box-shadow: 0 1px 6px rgba(79,110,247,.07);
    z-index: 10;
  }
  .header-left  { display: flex; align-items: center; gap: 12px; }
  .logo {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #4f6ef7, #7c3aed);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    box-shadow: 0 4px 12px rgba(79,110,247,.3);
    flex-shrink: 0;
  }
  .header-title { font-size: 1rem; font-weight: 800; color: #111827; }
  .header-title span { color: #4f6ef7; }
  .header-sub   { font-size: 0.68rem; color: #9ca3af; margin-top: 1px; }
  .chips { display: flex; gap: 6px; }
  .chip {
    background: #f3f4ff;
    border: 1px solid #dde3f8;
    color: #4f6ef7;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.67rem;
    font-weight: 600;
  }
  .status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #d1d5db;
    margin-left: 8px;
    transition: background .4s;
    flex-shrink: 0;
  }
  .status-dot.online  { background: #22c55e; box-shadow: 0 0 6px rgba(34,197,94,.5); }
  .status-dot.offline { background: #ef4444; }

  /* ── Chat area ── */
  #chat {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem 0;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    scroll-behavior: smooth;
  }
  #chat::-webkit-scrollbar { width: 4px; }
  #chat::-webkit-scrollbar-track { background: transparent; }
  #chat::-webkit-scrollbar-thumb { background: #c7d2fe; border-radius: 4px; }

  .chat-inner {
    max-width: 820px;
    width: 100%;
    margin: 0 auto;
    padding: 0 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  /* ── Empty state ── */
  .empty {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #9ca3af;
    padding: 3rem 1rem;
    text-align: center;
    gap: 0.5rem;
  }
  .empty .icon { font-size: 2.8rem; }
  .empty .title { font-size: 1rem; font-weight: 700; color: #374151; }
  .empty .sub   { font-size: 0.84rem; color: #9ca3af; }

  /* ── Messages ── */
  .msg { display: flex; gap: 10px; align-items: flex-end; }
  .msg.user { flex-direction: row-reverse; }

  .bubble {
    padding: 0.78rem 1.1rem;
    border-radius: 18px;
    font-size: 0.9rem;
    line-height: 1.72;
    max-width: 75%;
    word-break: break-word;
  }

  /* User bubble */
  .msg.user .bubble {
    background: linear-gradient(135deg, #4f6ef7, #7c3aed);
    color: #ffffff;
    border-radius: 20px 20px 4px 20px;
    box-shadow: 0 4px 16px rgba(79,110,247,.28);
  }

  /* Bot bubble */
  .msg.bot .bubble {
    background: #ffffff;
    color: #111827;
    border: 1px solid #dde3f8;
    border-radius: 4px 20px 20px 20px;
    box-shadow: 0 2px 10px rgba(79,110,247,.07);
  }

  /* Avatar */
  .avatar {
    width: 30px; height: 30px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
  }
  .msg.bot  .avatar { background: linear-gradient(135deg,#4f6ef7,#7c3aed); }
  .msg.user .avatar { background: #e0e7ff; }

  /* Timestamp */
  .ts { font-size: 0.64rem; color: #c4c9e0; margin-top: 3px; text-align: right; }
  .msg.bot .ts { text-align: left; }

  /* Markdown inside bot bubble */
  .bubble p   { margin: 0 0 0.4em; color: inherit; }
  .bubble p:last-child { margin-bottom: 0; }
  .bubble strong { font-weight: 700; color: inherit; }
  .bubble em     { font-style: italic; color: inherit; }
  .bubble ul, .bubble ol { padding-left: 1.2em; margin: 0.3em 0; }
  .bubble li { margin-bottom: 0.2em; color: inherit; }
  .bubble code {
    background: #eef2ff;
    color: #3b5bdb;
    border-radius: 5px;
    padding: 1px 6px;
    font-size: 0.83em;
    font-family: 'Fira Code', monospace;
  }
  .bubble pre {
    background: #1e293b;
    border-radius: 10px;
    padding: 12px 14px;
    overflow-x: auto;
    margin: 0.5em 0;
  }
  .bubble pre code {
    background: transparent;
    color: #e2e8f0;
    padding: 0;
    font-size: 0.84em;
  }

  /* Typing indicator */
  .typing { display: flex; gap: 5px; align-items: center; padding: 0.3rem 0; }
  .typing span {
    width: 7px; height: 7px;
    background: #c7d2fe;
    border-radius: 50%;
    animation: bounce 1.1s infinite;
  }
  .typing span:nth-child(2) { animation-delay: .18s; }
  .typing span:nth-child(3) { animation-delay: .36s; }
  @keyframes bounce {
    0%,80%,100% { transform:translateY(0); opacity:.5; }
    40%          { transform:translateY(-6px); opacity:1; }
  }

  /* ── Bottom input bar ── */
  .input-bar {
    background: #ffffff;
    border-top: 1px solid #e2e6f8;
    padding: 0.9rem 1.5rem 1rem;
    flex-shrink: 0;
    box-shadow: 0 -2px 12px rgba(79,110,247,.05);
  }
  .input-inner {
    max-width: 820px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
  }
  .input-box {
    background: #f5f7ff;
    border: 1.5px solid #dde3f8;
    border-radius: 14px;
    padding: 0.75rem 1rem;
    transition: border-color .15s, box-shadow .15s;
    display: flex;
    gap: 10px;
    align-items: flex-end;
  }
  .input-box:focus-within {
    border-color: #4f6ef7;
    box-shadow: 0 0 0 3px rgba(79,110,247,.1);
    background: #ffffff;
  }
  textarea {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    resize: none;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    font-size: 0.92rem;
    color: #111827;
    line-height: 1.6;
    min-height: 44px;
    max-height: 140px;
    overflow-y: auto;
  }
  textarea::placeholder { color: #9ca3af; }

  /* Send button */
  #send-btn {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #4f6ef7, #7c3aed);
    border: none;
    border-radius: 10px;
    color: #ffffff;
    font-size: 1.1rem;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(79,110,247,.35);
    transition: all .15s;
  }
  #send-btn:hover  { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(79,110,247,.45); }
  #send-btn:active { transform: translateY(0); }
  #send-btn:disabled { background: #c7d2fe; box-shadow: none; cursor: default; transform: none; }

  /* Controls row */
  .controls {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
  }
  .slider-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 1;
  }
  .slider-label { font-size: 0.75rem; color: #9ca3af; font-weight: 500; white-space: nowrap; }
  .slider-val   { font-size: 0.75rem; color: #4f6ef7; font-weight: 700; min-width: 16px; text-align: center; }
  input[type=range] {
    flex: 1;
    accent-color: #4f6ef7;
    height: 4px;
    cursor: pointer;
  }
  #clear-btn {
    background: transparent;
    border: 1px solid #e2e6f8;
    border-radius: 8px;
    color: #c4c9e0;
    font-size: 0.78rem;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    padding: 0.35rem 0.8rem;
    cursor: pointer;
    transition: all .15s;
    white-space: nowrap;
  }
  #clear-btn:hover { color: #ef4444; border-color: #fca5a5; background: #fff5f5; }

  /* ── Footer ── */
  footer {
    text-align: center;
    font-size: 0.68rem;
    color: #c4c9e0;
    padding: 0.25rem 0 0.4rem;
    flex-shrink: 0;
    background: #ffffff;
    border-top: none;
  }
  footer strong { color: #4f6ef7; }
</style>
</head>
<body>

<!-- TOP BAR -->
<header>
  <div class="header-left">
    <div class="logo">🤖</div>
    <div>
      <div class="header-title">AI <span>Programming</span> Assistant</div>
      <div class="header-sub">Powered by RAG · Ollama · Qdrant</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:12px;">
    <div class="chips">
      <span class="chip">🐍 Python</span>
      <span class="chip">🔥 PyTorch</span>
      <span class="chip">📐 TensorFlow</span>
      <span class="chip">🧠 ML</span>
    </div>
    <div class="status-dot" id="status-dot" title="API status"></div>
  </div>
</header>

<!-- CHAT -->
<div id="chat">
  <div class="chat-inner" id="chat-inner">
    <div class="empty" id="empty-state">
      <div class="icon">💬</div>
      <div class="title">How can I help you today?</div>
      <div class="sub">Ask anything about Python, PyTorch, TensorFlow or ML concepts.</div>
    </div>
  </div>
</div>

<!-- INPUT BAR -->
<div class="input-bar">
  <div class="input-inner">
    <div class="input-box">
      <textarea id="question" placeholder="Ask about Python, PyTorch, TensorFlow, ML concepts..." rows="2"></textarea>
      <button id="send-btn" title="Send">&#9650;</button>
    </div>
    <div class="controls">
      <div class="slider-wrap">
        <input type="range" id="sources-slider" min="3" max="15" value="5" step="1">
      </div>
      <button id="clear-btn">🗑 Clear</button>
    </div>
  </div>
</div>

<!-- FOOTER -->
<footer>
  <strong>CSAI-810 Project · Team 35</strong> &nbsp;·&nbsp;
  Osama Elkhuribi &amp; Esraa Nematalla
</footer>

<script>
// ── Simple markdown renderer ──────────────────
function renderMd(text) {
  return text
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    // code blocks first
    .replace(/```(\w*)\n?([\s\S]*?)```/g, (_,lang,code)=>
      `<pre><code class="${lang}">${code.trim()}</code></pre>`)
    // inline code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // bold / italic
    .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
    .replace(/\*(.+?)\*/g,'<em>$1</em>')
    // headers
    .replace(/^### (.+)$/gm,'<strong>$1</strong>')
    .replace(/^## (.+)$/gm,'<strong>$1</strong>')
    // lists
    .replace(/^\s*[-*] (.+)$/gm,'<li>$1</li>')
    .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
    // line breaks
    .replace(/\n{2,}/g,'</p><p>')
    .replace(/\n/g,'<br>')
    .replace(/^(.+)$/, '<p>$1</p>');
}

// ── Time ─────────────────────────────────────
function now() {
  return new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
}

// ── DOM refs ─────────────────────────────────
const chatInner  = document.getElementById('chat-inner');
const chatBox    = document.getElementById('chat');
const emptyState = document.getElementById('empty-state');
const textarea   = document.getElementById('question');
const sendBtn    = document.getElementById('send-btn');
const clearBtn   = document.getElementById('clear-btn');
const slider     = document.getElementById('sources-slider');

const statusDot  = document.getElementById('status-dot');

let msgCount = 0;

// ── Slider ───────────────────────────────────


// ── Auto-resize textarea ──────────────────────
textarea.addEventListener('input', () => {
  textarea.style.height = 'auto';
  textarea.style.height = Math.min(textarea.scrollHeight, 140) + 'px';
});

// ── Enter to send ─────────────────────────────
textarea.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
});

// ── Scroll to bottom ─────────────────────────
function scrollDown() {
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
}

// ── Add message bubble ────────────────────────
function addMsg(role, html, isHtml=false) {
  if (emptyState) emptyState.style.display = 'none';
  msgCount++;

  const wrap = document.createElement('div');
  wrap.className = `msg ${role}`;

  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = role === 'bot' ? '🤖' : '👤';

  const body = document.createElement('div');

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  if (isHtml) bubble.innerHTML = html;
  else bubble.textContent = html;

  const ts = document.createElement('div');
  ts.className = 'ts';
  ts.textContent = now();

  body.appendChild(bubble);
  body.appendChild(ts);

  if (role === 'bot') {
    wrap.appendChild(avatar);
    wrap.appendChild(body);
  } else {
    wrap.appendChild(body);
    wrap.appendChild(avatar);
  }

  chatInner.appendChild(wrap);
  scrollDown();
  return bubble; // return for updating (typing indicator)
}

// ── Typing indicator ─────────────────────────
function addTyping() {
  if (emptyState) emptyState.style.display = 'none';
  const wrap = document.createElement('div');
  wrap.className = 'msg bot';
  wrap.id = 'typing-indicator';

  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = '🤖';

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.innerHTML = '<div class="typing"><span></span><span></span><span></span></div>';

  wrap.appendChild(avatar);
  wrap.appendChild(bubble);
  chatInner.appendChild(wrap);
  scrollDown();
}

function removeTyping() {
  const t = document.getElementById('typing-indicator');
  if (t) t.remove();
}

// ── Send ─────────────────────────────────────
async function send() {
  const q = textarea.value.trim();
  if (!q) return;

  textarea.value = '';
  textarea.style.height = 'auto';
  sendBtn.disabled = true;

  addMsg('user', q);
  addTyping();

  try {
    const res = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q, num_sources: parseInt(slider.value) })
    });
    const data = await res.json();
    removeTyping();

    if (res.ok && data.answer) {
      addMsg('bot', renderMd(data.answer), true);
    } else {
      addMsg('bot', `⚠️ ${data.error || 'Something went wrong'}`, false);
    }
  } catch(e) {
    removeTyping();
    addMsg('bot', '⚠️ Cannot reach the server. Is the backend running?', false);
  }

  sendBtn.disabled = false;
  textarea.focus();
}

sendBtn.addEventListener('click', send);

// ── Clear ────────────────────────────────────
clearBtn.addEventListener('click', () => {
  chatInner.innerHTML = '';
  chatInner.appendChild(emptyState);
  emptyState.style.display = 'flex';
  msgCount = 0;
});

// ── Health check ─────────────────────────────
async function checkHealth() {
  try {
    const r = await fetch('/health');
    const d = await r.json();
    statusDot.className = 'status-dot ' + (d.online ? 'online' : 'offline');
  } catch {
    statusDot.className = 'status-dot offline';
  }
}
checkHealth();
setInterval(checkHealth, 15000);
</script>
</body>
</html>"""


if __name__ == "__main__":
    print("🤖 AI Programming Assistant")
    print("   Open: http://localhost:8080")
    print("   Make sure FastAPI is running on port 5000")
    app.run(host="0.0.0.0", port=8080, debug=False)
