from flask import Flask, render_template, request, jsonify
from src.helper import (
    download_hugging_face_embeddings,
    extract_unique_remedies_from_pdf
)
from langchain_pinecone import PineconeVectorStore
from langchain_community.llms import Cohere
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

# Load embeddings and setup vector store
embeddings = download_hugging_face_embeddings()
index_name = "swasthabot"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# LLM & chain setup
llm = Cohere(
    model="command-r-plus",
    cohere_api_key=COHERE_API_KEY,
    max_tokens=1500,
    temperature=0.5
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Dynamically load known remedies from Charak Samhita
known_remedies = extract_unique_remedies_from_pdf()

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    print("User:", msg)

    response = rag_chain.invoke({"input": msg})
    print("=== Full Response ===")
    print(response)

    answer = response.get("answer", "").strip()
    if not answer or answer.lower() in ["i don't know", ""]:
        fallback = "I'm not sure about that. Try rephrasing or ask something health-related."
        print("Fallback Response:", fallback)
        return jsonify({"reply": fallback})

    print("RAG Chain Response:", answer)
    formatted_answer = answer.replace("\n", "<br>")
    return jsonify({"reply": formatted_answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
