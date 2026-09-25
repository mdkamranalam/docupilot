import streamlit as st
import requests
import time

API_BASE_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="DocuPilot — AI Document Intelligence",
    page_icon="📄",
    layout="wide"
)

# Custom Styling for polished UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        color: #1E293B;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .source-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px;
        margin-top: 8px;
        font-size: 0.88rem;
    }
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        background-color: #EEF2F6;
        color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_doc_id" not in st.session_state:
    st.session_state.selected_doc_id = None


def fetch_documents():
    try:
        res = requests.get(f"{API_BASE_URL}/documents", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []


# --- SIDEBAR: Document Management ---
with st.sidebar:
    st.title("📁 Document Vault")
    st.caption("Upload PDF, TXT, or Markdown documents to index.")

    uploaded_file = st.file_uploader(
        "Upload Document",
        type=["pdf", "txt", "md"],
        help="Supported formats: PDF, TXT, MD"
    )

    if uploaded_file is not None:
        if st.button("🚀 Process & Index Document", use_container_width=True):
            with st.spinner("Parsing, chunking, and embedding vectors..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    resp = requests.post(f"{API_BASE_URL}/documents/upload", files=files)
                    if resp.status_code == 200:
                        st.success(f"Indexed '{uploaded_file.name}' successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Error: {resp.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")

    st.divider()
    st.subheader("📚 Active Documents")
    docs = fetch_documents()

    if not docs:
        st.info("No documents uploaded yet.")
    else:
        doc_options = {"All Documents": None}
        for d in docs:
            doc_options[f"{d['filename']} ({d['chunks_count']} chunks)"] = d["id"]

        selected_label = st.selectbox("Focus query on:", list(doc_options.keys()))
        st.session_state.selected_doc_id = doc_options[selected_label]

        st.write("---")
        for d in docs:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"📄 **{d['filename']}**")
                st.caption(f"{d['chunks_count']} chunks")
            with col2:
                if st.button("🗑️", key=f"del_{d['id']}"):
                    requests.delete(f"{API_BASE_URL}/documents/{d['id']}")
                    st.rerun()


# --- MAIN PANEL: Chat Assistant ---
st.markdown('<div class="main-header">DocuPilot Knowledge Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ask questions across your uploaded knowledge base with exact source citations.</div>', unsafe_allow_html=True)

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("🔍 View Referenced Sources"):
                for s in msg["sources"]:
                    st.markdown(
                        f"""
                        <div class="source-card">
                            <div><strong>📄 {s['filename']}</strong> | <span class="badge">Page {s['page']}</span> | <span class="badge">Similarity: {s['similarity_score']}</span></div>
                            <div style="margin-top: 6px; color: #475569;"><em>"{s['excerpt']}"</em></div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

# Input Box
if user_input := st.chat_input("Ask a question about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("Retrieving grounded context and formulating answer..."):
            try:
                # Prepare conversation history
                history = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages[:-1]
                ]

                payload = {
                    "question": user_input,
                    "document_id": st.session_state.selected_doc_id,
                    "conversation_history": history,
                    "top_k": 4
                }

                resp = requests.post(f"{API_BASE_URL}/chat/query", json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    answer_text = data["answer"]
                    sources = data.get("sources", [])

                    st.write(answer_text)

                    if sources:
                        with st.expander("🔍 View Referenced Sources"):
                            for s in sources:
                                st.markdown(
                                    f"""
                                    <div class="source-card">
                                        <div><strong>📄 {s['filename']}</strong> | <span class="badge">Page {s['page']}</span> | <span class="badge">Similarity: {s['similarity_score']}</span></div>
                                        <div style="margin-top: 6px; color: #475569;"><em>"{s['excerpt']}"</em></div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer_text,
                        "sources": sources
                    })
                else:
                    err_msg = f"Backend Error: {resp.text}"
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
            except Exception as e:
                err_msg = f"Connection failed: {e}. Is the FastAPI server running?"
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})
