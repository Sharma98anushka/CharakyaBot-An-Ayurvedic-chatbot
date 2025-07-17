## CharakyaBot-An-Ayurvedic-chatbot
An AI-powered Swastha designed to provide accurate, real-time, and context-aware responses to health-related queries. Built with Cohere’s LLM for natural language processing and Pinecone’s vector search for efficient medical information retrieval, this chatbot serves as a smart virtual assistant for users seeking reliable home care insights.

### Features
> AI-Powered Responses: Uses Cohere's LLM to generate human-like answers.
> Smart Information Retrieval: Fetches the most relevant ayurvedic info from Pinecone.
> Seamless Web Interface: Built with Flask, providing an easy-to-use chatbot UI.
> Secure API Integration: Keeps credentials safe with .env configuration.

### Tech Stack
Cohere LLM – For query understanding and natural language generation

LangChain – For building the RAG pipeline and chaining retrieval + generation steps

Pinecone – For fast and accurate semantic vector search

Flask – Backend server to handle query-routing and frontend interactions

PDF Preprocessing – Used to parse and clean the Charak Samhita for vector indexing 
