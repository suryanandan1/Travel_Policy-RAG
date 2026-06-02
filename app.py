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

    domestic_split = split_documents(domestic_docs)
    foreign_split = split_documents(foreign_docs)

    domestic_vectorstore = create_vectorstore(domestic_split)
    foreign_vectorstore = create_vectorstore(foreign_split)

    domestic_qa = build_qa_chain(domestic_vectorstore)
    foreign_qa = build_qa_chain(foreign_vectorstore)

    return domestic_qa, foreign_qa


domestic_qa, foreign_qa = load_system()


if "messages" not in st.session_state:
    st.session_state.messages = []

# show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


query = st.chat_input("Ask your travel policy question...")

if query:
    # show user message
    st.chat_message("user").write(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # choose correct chain
    if "foreign" in query.lower() or "abroad" in query.lower():
        qa_chain = foreign_qa
    else:
        qa_chain = domestic_qa

    # get answer
    response = qa_chain.invoke({"query": query})
    answer = response["result"].replace("**", "")

    # show assistant response
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})