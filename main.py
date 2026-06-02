from loaders import load_pdfs
from splitter import split_documents
from embeddings_store import create_vectorstore
from qa_chain import build_qa_chain


domestic_docs = load_pdfs(["data/domestic_travel.pdf"])
foreign_docs = load_pdfs(["data/foreign_travel.pdf"])

domestic_split = split_documents(domestic_docs)
foreign_split = split_documents(foreign_docs)

domestic_vectorstore = create_vectorstore(domestic_split)
foreign_vectorstore = create_vectorstore(foreign_split)

domestic_qa = build_qa_chain(domestic_vectorstore)
foreign_qa = build_qa_chain(foreign_vectorstore)


while True:
    query = input("\nEnter your query (or type 'exit'): ")

    if query.lower() == "exit":
        break

    if "foreign" in query.lower() or "abroad" in query.lower():
        qa_chain = foreign_qa
    else:
        qa_chain = domestic_qa

    response = qa_chain.invoke({"query": query})

    # print("\n===== RETRIEVED CHUNKS =====")

    # for i, doc in enumerate(response["source_documents"]):
    #     print(f"\nCHUNK {i+1}")
    #     print(doc.page_content[:1200])

    answer = response["result"].replace("**", "")

    print("\nAnswer:")
    print(answer)