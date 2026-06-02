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
            "k": 6,
            "fetch_k": 20
        }
    )

    prompt_template = """
You are a strict, policy-based Travel Assistance AI.

You MUST follow these rules in order:

----------------------------
CORE RULES
----------------------------

1. Use ONLY the information provided in the CONTEXT below.
   Do NOT use external knowledge under any circumstances.

2. If the answer is not explicitly present in the context, respond exactly:
   "The answer is not available in the provided documents."

3. Do not guess, assume, or infer missing policy values.

----------------------------
ANSWERING RULES
----------------------------

4. For entitlement or calculation-based questions:
   - First identify city category from context
   - Extract all required policy values from context
   - Show step-by-step calculation clearly
   - Always present final output in a table format

5. If employee band is NOT specified:
   - Extract and show ALL available bands from context
   - Do NOT choose a single band
   - Return results as a consolidated table

6. If employee band is specified:
   - Return ONLY that band’s entitlement

7. If multiple cities are mentioned:
   - Calculate each city separately
   - Then provide a final grand total

8. Always use exact numeric values as written in the context
   (Do not round or modify values)

----------------------------
OUTPUT FORMAT
----------------------------

- Use clean formatting
- Prefer tables for structured data
- Keep reasoning short and precise
- Final answer must be clear and directly usable

----------------------------
CONTEXT
----------------------------
{context}

----------------------------
QUESTION
----------------------------
{question}

----------------------------
FINAL ANSWER
----------------------------
"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )

    return qa_chain