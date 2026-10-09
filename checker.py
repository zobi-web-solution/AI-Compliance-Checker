# checker.py
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

COLLECTION = "compliance_docs"

COMPLIANCE_PROMPT = ChatPromptTemplate.from_template("""
You are a strict compliance officer. Using ONLY the policy documents provided below,
assess whether the described action or scenario is compliant.

Policy context:
{context}

Scenario to assess:
{question}

Respond in this exact structure:
VERDICT: [COMPLIANT / NON-COMPLIANT / UNCLEAR]
REASON: [1-2 sentences explaining why]
RELEVANT CLAUSE: [Quote the exact policy clause that applies]
RECOMMENDATION: [What action should be taken, if any]
""")

def build_chain():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=COLLECTION,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    llm = OllamaLLM(model="llama3.2", temperature=0)

    def format_docs(docs):
        return "\n\n---\n\n".join(
            f"[Source: {d.metadata.get('source','?')}]\n{d.page_content}"
            for d in docs
        )

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | COMPLIANCE_PROMPT
        | llm
    )
    return chain

def check(scenario: str):
    chain = build_chain()
    result = chain.invoke(scenario)
    return result

if __name__ == "__main__":
    scenarios = [
        "We plan to share employee salary details with third party vendors.",
        "Employees are allowed to work from home without manager approval.",
    ]
    for s in scenarios:
        print(f"\n{'='*60}")
        print(f"SCENARIO: {s}")
        print(f"{'='*60}")
        print(check(s))