import streamlit as st

from loaders import load_pdfs
from splitter import split_documents
from embeddings_store import create_vectorstore
from qa_chain import build_qa_chain


st.set_page_config(page_title="Travel Policy RAG", layout="wide")
st.title("Travel Policy Assistant (RAG)")


@st.cache_resource
def load_system():
    domestic_docs = load_pdfs(["data/domestic_travel.pdf"])
    foreign_docs = load_pdfs(["data/foreign_travel.pdf"])

    all_docs = domestic_docs + foreign_docs
    all_split = split_documents(all_docs)

    vectorstore = create_vectorstore(all_split)

    qa_chain = build_qa_chain(vectorstore)

    return qa_chain


qa_chain = load_system()

if "messages" not in st.session_state:
    st.session_state.messages = []


# chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


query = st.chat_input("Ask your travel policy question...")

if query:
    st.chat_message("user").write(query)
    st.session_state.messages.append({"role": "user", "content": query})

    response = qa_chain.invoke({"query": query})
    answer = response["result"].replace("**", "")

    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})