from langchain_mistralai import ChatMistralAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os


def build_qa_chain(vectorstore):
    load_dotenv()

    model = ChatMistralAI(
        api_key=os.getenv("MISTRAL_API_KEY"),
        model="mistral-large-latest",
        temperature=0
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 15,
            "fetch_k": 40
        }
    )

    prompt_template = """
You are a strict document-based travel policy assistant.

Rules:

1. Answer ONLY from the provided context.

2. Never assume or invent information.

3. If information is unavailable, respond:
"The answer is not available in the provided documents."

4. For entitlement calculations:
   - Identify city category first.
   - Show calculations clearly.
   - Use tables whenever possible.

5. If employee band is NOT specified:
   - Show ALL bands found in the context.
   - Never choose a single band.
   - Present results in a consolidated table.

6. If employee band IS specified:
   - Show only that band's entitlement.

7. When multiple cities are involved:
   - Calculate each city separately.
   - Then show grand total.

8. Always use policy values exactly as provided.

Context:
{context}

Question:
{question}

Answer:
"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=model,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )

    return qa_chain