from typing import List
from backend.app.config import OPENAI_API_KEY

try:
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.docstore.document import Document
    from langchain.chat_models import ChatOpenAI
    from langchain.chains import RetrievalQA
except Exception:  # pragma: no cover - optional dependency
    OpenAIEmbeddings = None
    FAISS = None
    Document = None
    ChatOpenAI = None
    RetrievalQA = None


def _chunk_text(text: str, chunk_size: int = 1000) -> List[Document]:
    docs: List[Document] = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i : i + chunk_size]
        docs.append(Document(page_content=chunk))
    return docs


def rag_answer(document_text: str, question: str, k: int = 4) -> dict:
    if OpenAIEmbeddings is None:
        raise RuntimeError("LangChain or its dependencies are not installed")

    docs = _chunk_text(document_text)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    index = FAISS.from_documents(docs, embeddings)
    retriever = index.as_retriever(search_kwargs={"k": k})
    llm = ChatOpenAI(temperature=0.2, model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    answer = qa_chain.run(question)
    return {"answer": answer}
