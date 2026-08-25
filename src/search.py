import os
from dotenv import load_dotenv
from src.vectorstore import FaissVectorStore
from langchain_groq import ChatGroq
from groq import Groq

load_dotenv()


class RAGSearch:
    def __init__(self, persist_dir: str="faiss_store", embedding_model: str = "all-MiniLM-L6-v2", llm_model: str = "openai/gpt-oss-20b"):
        self.vectorstore= FaissVectorStore(persist_dir, embedding_model)
        #Load or build vectorstore
        faiss_path= os.path.join(persist_dir, "faiss.index")
        meta_path= os.path.join(persist_dir, "metadata.pkl")

        if not (os.path.exists(meta_path) and os.path.exists(faiss_path)):
            from src.data_loader import load_all_documents
            docs= load_all_documents("data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
        groq_api_key = os.getenv("GROQ_API_KEY")

        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=llm_model,
           
            )
        print(f"[INFO] Groq LLM initialized: {llm_model}")

    def search_and_summarize(self, query:str, top_k:int= 5) -> str:
        results= self.vectorstore.query(query, top_k=top_k)
        texts=  [ r["metadata"].get("text","") for r in results if r["metadata"]]
        context= "\n\n".join(texts)
        if not context:
            return "No relevant documents found."
        prompt = f"""
            You are a helpful and knowledgeable RAG assistant.

            Answer the user's question using ONLY the provided context.

            Give a detailed, comprehensive answer. Do not give a short summary unless
            the user specifically asks for a short answer.

            Explain the topic clearly and include:
            - A direct definition or answer
            - Important details from the context
            - How the concept works or is used
            - Relevant components, steps, treatments, methods, or examples mentioned
            in the context
            - Important comparisons or distinctions when present
            - Any relevant findings or conclusions from the context

            Organize the answer using paragraphs and bullet points where appropriate.

            Do not invent information that is not present in the context.
            If the context does not contain enough information to answer a part of the
            question, explicitly say that the information is not available in the
            provided documents.

            Question:
            {query}

            Context:
            {context}

            Detailed Answer:
            """
        response= self.llm.invoke([prompt])
        return response.content

#