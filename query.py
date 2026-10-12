import os
from dotenv import load_dotenv
from pinecone import Pinecone
# from fastapi import FastAPI
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))


index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

vectorstore = PineconeVectorStore(
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    namespace="mysyllabus",
    embedding=embeddings
)

retriever =  vectorstore.as_retriever(
    search_kwargs={"k" : 4}
)


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


prompt = ChatPromptTemplate.from_template("""
Use ONLY the following context to answer the question.
if the question is proper and in boundaries to the context provided, be very gentle and comapssionate else if the answer is not in the context, be extremely rude and make fun of their stupidity in an extreme dark way!
Context:
{context}

Question:
{question}
""")

rag_chain = (
    RunnableMap({
        "context": retriever,
        "question": RunnablePassthrough()
    })
    | prompt
    | llm
)

# class Query(BaseModel):
#     question: str

# app = FastAPI()

# @app.post("/rag")
# def ask_rag(q: Query):
#     answer = rag_chain.invoke(q.question)
#     return {"answer": answer.content}