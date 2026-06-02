from loaders import load_pdfs
from splitter import split_documents
from embeddings_store import create_vectorstore
from qa_chain import build_qa_chain


# Load both PDFs
domestic_docs = load_pdfs(["data/domestic_travel.pdf"])
foreign_docs = load_pdfs(["data/foreign_travel.pdf"])

# Merge documents
all_docs = domestic_docs + foreign_docs

# Split
all_split = split_documents(all_docs)

# Vector store (SINGLE INDEX)
vectorstore = create_vectorstore(all_split)

# QA chain (SINGLE CHAIN)
qa_chain = build_qa_chain(vectorstore)


while True:
    query = input("\nEnter your query (or type 'exit'): ")

    if query.lower() == "exit":
        break

    response = qa_chain.invoke({"query": query})

    answer = response["result"].replace("**", "")

    print("\nAnswer:")
    print(answer)

    # OPTIONAL: debug sources
    # for doc in response["source_documents"]:
    #     print(doc.metadata)