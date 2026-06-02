# build_vector_db.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Ripping out Google and using FastEmbed locally
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_qdrant import QdrantVectorStore

def build_database():
    print("1. Loading the Support Manual...")
    with open("support_manual.txt", "r", encoding="utf-8") as f:
        manual_text = f.read()

    print("2. Chopping the manual into readable chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(manual_text)

    print("3. Firing up Local FastEmbed (Zero API calls!)...")
    # This runs 100% locally on your machine. No Google rate limits or 404s.
    embeddings = FastEmbedEmbeddings()

    print("4. Building the local Qdrant Vector Database...")
    # Creates a local folder called "qdrant_db"
    QdrantVectorStore.from_texts(
        texts=chunks,
        embedding=embeddings,
        path="./qdrant_db",
        collection_name="support_manual"
    )

    print("✅ Vector Database built successfully! (./qdrant_db)")

if __name__ == "__main__":
    build_database()