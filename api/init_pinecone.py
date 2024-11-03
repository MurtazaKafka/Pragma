from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

def init_pinecone():
    load_dotenv()
    
    try:
        # Initialize Pinecone client
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        
        # Define index name
        index_name = os.getenv("PINECONE_INDEX_NAME")
        
        # Check if index already exists
        existing_indexes = pc.list_indexes()
        
        if index_name not in existing_indexes:
            # Create index if it doesn't exist
            pc.create_index(
                name=index_name,
                dimension=1536,  # OpenAI ada-002 embedding dimension
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-west-2'
                )
            )
            print(f"Created new Pinecone index: {index_name}")
        else:
            print(f"Pinecone index {index_name} already exists")
            
        # Test connection to index
        index = pc.Index(index_name)
        stats = index.describe_index_stats()
        print(f"Successfully connected to index. Current stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"Error initializing Pinecone: {str(e)}")
        return False

if __name__ == "__main__":
    init_pinecone()