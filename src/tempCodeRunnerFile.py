import json
import random
import re
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings


def load_pdf_file(data):
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

def download_hugging_face_embeddings():
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

def load_intent_responses(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data["questions"]

def get_intent_response(user_input, intent_data):
    user_input = user_input.lower()
    for intent in intent_data:
        for pattern in intent["patterns"]:
            if re.fullmatch(pattern, user_input) or re.search(pattern, user_input):
                return random.choice(intent["responses"])
    return None
