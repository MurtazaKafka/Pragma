from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

def create_pinecone_index():
    load_dotenv()
    
    # Initialize Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    
    # Define index configuration
    index_name = "financial-data-rag"
    
    # Check if index already exists
    existing_indexes = pc.list_indexes()
    
    if index_name not in existing_indexes:
        # Create the index with appropriate configuration
        pc.create_index(
            name=index_name,
            dimension=1536,  # Dimension for text-embedding-ada-002 model
            metric="cosine",  # Cosine similarity is best for semantic search
            spec=ServerlessSpec(
                cloud="aws",
                region="us-west-2"
            ),
            metadata_config={
                "indexed": [
                    # Fields we want to filter on
                    "question",
                    "organization",
                    "content_type",
                    "timestamp",
                    "source_url"
                ]
            }
        )
        print(f"Created new index: {index_name}")
    else:
        print(f"Index {index_name} already exists")
    
    # Return the index for immediate use
    return pc.Index(index_name)

def define_sample_vector():
    """
    Define the structure of vectors to be stored in the index
    This serves as documentation for the expected vector format
    """
    sample_vector = {
        "id": "unique_vector_id",  # Hash of question + organization + url
        "values": [0.0] * 1536,    # Your actual embedding values
        "metadata": {
            "question": "What is the financial performance?",
            "organization": "Company XYZ",
            "content_type": "financial_report",  # Type of content
            "timestamp": "2024-03-15T10:30:00Z",  # When the data was collected
            "source_url": "https://example.com/data",
            "content": "The actual text content...",
            "relevance_score": 0.95,  # Optional relevance score
        }
    }
    return sample_vector

def create_index_management_functions():
    """
    Helper functions for managing the index
    """
    def delete_old_data(index, organization, days_old=30):
        """Delete vectors older than specified days"""
        import datetime
        cutoff_date = (datetime.datetime.utcnow() - 
                      datetime.timedelta(days=days_old)).isoformat()
        
        index.delete(
            filter={
                "organization": organization,
                "timestamp": {"$lt": cutoff_date}
            }
        )
    
    def update_organization_data(index, organization, new_vectors):
        """Update all data for a specific organization"""
        # First delete existing data for the organization
        index.delete(filter={"organization": organization})
        # Then upsert new vectors
        index.upsert(vectors=new_vectors)
    
    return {
        "delete_old_data": delete_old_data,
        "update_organization_data": update_organization_data
    }

# Example usage:
if __name__ == "__main__":
    # Create or get existing index
    index = create_pinecone_index()
    
    # Get management functions
    index_management = create_index_management_functions()
    
    # Example of how to use the index
    sample_vector = define_sample_vector()
    print(f"Sample vector structure: {sample_vector}")
    
    # Example of updating organization data
    # index_management["update_organization_data"](
    #     index, 
    #     "Company XYZ", 
    #     [sample_vector]
    # )