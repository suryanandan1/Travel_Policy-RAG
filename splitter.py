from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=500
    )

    return text_splitter.split_documents(docs)