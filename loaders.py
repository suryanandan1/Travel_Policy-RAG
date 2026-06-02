from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document


def load_pdfs(pdf_files):
    docs = []

    for pdf in pdf_files:
        loader = PyPDFLoader(pdf)
        pages = loader.load()

        full_text = "\n\n".join(page.page_content for page in pages)

        docs.append(
            Document(
                page_content=full_text,
                metadata={"source_file": pdf}
            )
        )

    return docs