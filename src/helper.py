import json
import random
import re
import fitz  # PyMuPDF
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings


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

def extract_unique_remedies_from_pdf(pdf_path="data/charak_samhita.pdf"):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()

        # Simple regex: Capture words starting with a capital letter (e.g., Ashwagandha, Triphala)
        matches = re.findall(r'\b[A-Z][a-z]{2,}\b', text)
        remedies = list(set(matches))
        return sorted(remedies)
    except Exception as e:
        print(f"Error extracting remedies: {e}")
        return []
