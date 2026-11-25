"""Streamlit web app: upload a PDF, ask questions, see the cited pages.

Run from this folder:  streamlit run app.py
"""
import hashlib
import os
import tempfile

import streamlit as st

from rag import answer, build_index, load_pdf

st.set_page_config(page_title="Document Q&A · 文档问答", layout="centered")
st.title("Document Q&A · 文档问答")
st.caption("Upload a PDF, then ask questions. Every answer cites the pages it came from. "
           "上传 PDF 后提问，每个回答都标注出处页码。")


@st.cache_resource(show_spinner=False)
def index_for(file_hash: str, _data: bytes):
    """Build the search index once per file (cached by the file's hash)."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(_data)
        path = f.name
    try:
        chunks = load_pdf(path)
    finally:
        os.remove(path)
    if not chunks:
        raise ValueError("No text found in this PDF. Scanned PDFs need OCR first.")
    pages = len({c.metadata["page_number"] for c in chunks})
    return build_index(chunks), len(chunks), pages


uploaded = st.file_uploader("PDF file · PDF 文件", type=["pdf"])
if not uploaded:
    st.info("Upload a PDF to start. · 请先上传 PDF。")
    st.stop()

data = uploaded.getvalue()
file_hash = hashlib.sha256(data).hexdigest()
try:
    with st.spinner("Reading and indexing the document… · 正在解析文档…"):
        store, n_chunks, n_pages = index_for(file_hash, data)
except Exception as e:
    st.error(f"Could not index this file: {e}")
    st.stop()
st.success(f"Ready: {uploaded.name} · {n_pages} pages · {n_chunks} passages")

history = st.session_state.setdefault(file_hash, [])
for turn in history:
    with st.chat_message("user"):
        st.write(turn["question"])
    with st.chat_message("assistant"):
        st.write(turn["answer"])
        if turn["found"]:
            st.caption("Pages cited · 引用页码: " + (", ".join(map(str, turn["cited_pages"])) or "—"))

question = st.chat_input("Ask about the document · 输入问题")
if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking… · 思考中…"):
                result = answer(store, question)
        except Exception as e:
            st.error(f"The model call failed: {e}")
            st.stop()
        st.write(result["answer"])
        if result["found"]:
            st.caption("Pages cited · 引用页码: " + (", ".join(map(str, result["cited_pages"])) or "—"))
            with st.expander("Source passages · 原文片段"):
                for s in result["sources"]:
                    st.markdown(f"**p.{s['page']}**")
                    st.text(s["text"][:500])
    history.append({"question": question, **result})
