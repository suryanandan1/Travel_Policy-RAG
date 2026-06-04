import streamlit as st

st.set_page_config(
    page_title="Travel Policy Assistant",
    layout="wide"
)

from login import login_page
from loaders import load_pdfs
from splitter import split_documents
from embeddings_store import create_vectorstore
from qa_chain import build_qa_chain


# ---------------- SESSION ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- LOGIN SCREEN ---------------- #

if not st.session_state.logged_in:
    login_page()
    st.stop()


# ---------------- RAG LOADING ---------------- #

@st.cache_resource
def load_system():

    domestic_docs = load_pdfs(
        ["data/domestic_travel.pdf"]
    )

    foreign_docs = load_pdfs(
        ["data/foreign_travel.pdf"]
    )

    all_docs = domestic_docs + foreign_docs

    all_split = split_documents(all_docs)

    vectorstore = create_vectorstore(all_split)

    qa_chain = build_qa_chain(vectorstore)

    return qa_chain


qa_chain = load_system()


# ---------------- UI ---------------- #

user = st.session_state.user

st.title("Travel Policy Assistant")

st.sidebar.success(
    f"""
    Logged in as: {user['name']}

    Band: {user['band']}
    """
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.messages = []

    st.rerun()


# ---------------- CHAT HISTORY ---------------- #

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ---------------- CHAT INPUT ---------------- #

query = st.chat_input(
    "Ask your travel policy question..."
)

if query:

    st.chat_message("user").write(query)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    band = user["band"]

    enhanced_query = f"""
Employee Band: {band}

User Question:
{query}

Important:
- Answer only for this employee band.
- Do not provide entitlements for other bands.
- Use the travel policy documents only.
"""

    response = qa_chain.invoke(
        {"query": enhanced_query}
    )

    answer = response["result"].replace("**", "")

    st.chat_message("assistant").write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )