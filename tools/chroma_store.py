import os
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

class KnowledgeBase:
    def __init__(self, persist_directory="./chroma_db"):
        # Create a persistent client that saves data to the specified directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize the OpenAI embedding function
        self.embedding_fn = OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )
        
        # Get or create a collection for company policies
        self.collection = self.client.get_or_create_collection(
            name="company_sops",
            embedding_function=self.embedding_fn
        )

    def add_sop(self, sop_id: str, text: str, metadata: dict = None):
        """Adds a standard operating procedure to the vector database."""
        self.collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[sop_id]
        )

    def query_sop(self, query: str, n_results: int = 1):
        """Allows the research agent to query relevant policies."""
        return self.collection.query(
            query_texts=[query],
            n_results=n_results
        )