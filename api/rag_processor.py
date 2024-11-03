from typing import List, Dict
import os
from dataclasses import dataclass
import json
import pandas as pd
from openai import OpenAI
from pinecone import Pinecone, Index
from dotenv import load_dotenv

@dataclass
class SearchResult:
    question: str
    organization: str
    content: str
    url: str

@dataclass
class ProcessedResult:
    question: str
    organization: str
    answer: Dict

class RAGProcessor:
    def __init__(self):
        load_dotenv()
        
        # Validate environment variables
        required_vars = ["OPENAI_API_KEY", "PINECONE_API_KEY", "PINECONE_ENV", "PINECONE_INDEX_NAME"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize Pinecone with environment
        self.pc = Pinecone(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENV")
        )
        
        # Get or create index
        index_name = os.getenv("PINECONE_INDEX_NAME")
        try:
            self.index = self.pc.Index(index_name)
        except Exception as e:
            # If index doesn't exist, create it
            self.pc.create_index(
                name=index_name,
                dimension=1536,  # dimension for text-embedding-ada-002
                metric="cosine"
            )
            self.index = self.pc.Index(index_name)

    def vectorize_content(self, search_results: List[SearchResult]) -> List[Dict]:
        """Convert scraped content into embeddings and store in vector format"""
        vectors = []
        
        for result in search_results:
            try:
                # Ensure content is not too long for OpenAI's token limit
                content = result.content[:8000]  # Truncate to avoid token limits
                
                # Generate embedding using OpenAI
                response = self.openai_client.embeddings.create(
                    input=content,
                    model="text-embedding-ada-002"
                )
                embedding = response.data[0].embedding
                
                # Convert URL to string if it's a Pydantic URL object
                url_str = str(result.url)
                
                # Create a unique ID that's consistent and URL-safe
                unique_id = f"{hash(result.question + result.organization + url_str)}"
                
                # Create metadata for the vector
                metadata = {
                    "question": result.question,
                    "organization": result.organization,
                    "content": content,
                    "url": url_str
                }
                
                vectors.append({
                    "id": unique_id,
                    "values": embedding,
                    "metadata": metadata
                })
            except Exception as e:
                print(f"Error vectorizing content for {url_str}: {str(e)}")
                continue
        
        return vectors

    def store_vectors(self, vectors: List[Dict]):
        """Store vectors in Pinecone"""
        if not vectors:
            return
            
        try:
            # Upsert vectors in batches of 100
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
        except Exception as e:
            print(f"Error storing vectors: {str(e)}")
            raise

    def query_vector_db(self, question: str, organization: str, top_k: int = 3) -> List[Dict]:
        """Query vector database for relevant content"""
        try:
            # Generate query embedding
            query_text = f"Question: {question} Organization: {organization}"
            query_embedding = self.openai_client.embeddings.create(
                input=query_text,
                model="text-embedding-ada-002"
            ).data[0].embedding
            
            # Query Pinecone with metadata filtering
            results = self.index.query(
                vector=query_embedding,
                filter={
                    "question": {"$eq": question},
                    "organization": {"$eq": organization}
                },
                top_k=top_k,
                include_metadata=True
            )
            
            return results.matches
        except Exception as e:
            print(f"Error querying vector database: {str(e)}")
            return []

    def process_with_llm(self, query_results: List[Dict], question: str) -> Dict:
        """Process retrieved content with LLM"""
        try:
            # Construct prompt with retrieved content
            context = "\n\n".join([
                f"Source {i+1}:\n{result.metadata['content']}"
                for i, result in enumerate(query_results)
            ])
            
            prompt = f"""Based on the following sources, answer the question: "{question}"
            
            {context}
            
            Provide your response in the following JSON format:
            {{
                "answer": "A comprehensive answer",
                "key_findings": ["finding 1", "finding 2", ...],
                "confidence_score": 0.0 to 1.0,
                "sources": ["url1", "url2", ...]
            }}"""
            
            # Get LLM response
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error processing with LLM: {str(e)}")
            return {
                "answer": "Error processing response",
                "key_findings": [],
                "confidence_score": 0.0,
                "sources": []
            }

    async def process_data_matrix(
        self,
        questions: List[str],
        organizations: List[str],
        search_results: List[SearchResult]
    ) -> pd.DataFrame:
        """Process entire matrix of questions and organizations"""
        try:
            # Vectorize and store all search results
            vectors = self.vectorize_content(search_results)
            if vectors:
                self.store_vectors(vectors)
            
            # Process each question-organization pair
            results = []
            for question in questions:
                for org in organizations:
                    # Query vector DB
                    relevant_content = self.query_vector_db(question, org)
                    
                    # Process with LLM
                    processed_result = self.process_with_llm(relevant_content, question)
                    
                    results.append(ProcessedResult(
                        question=question,
                        organization=org,
                        answer=processed_result
                    ))
            
            # Convert results to DataFrame
            df_data = []
            for result in results:
                row = {
                    'Question': result.question,
                    'Organization': result.organization,
                    'Answer': result.answer['answer'],
                    'Key Findings': '; '.join(result.answer['key_findings']),
                    'Confidence': result.answer['confidence_score'],
                    'Sources': '; '.join(result.answer['sources'])
                }
                df_data.append(row)
            
            return pd.DataFrame(df_data)
        except Exception as e:
            print(f"Error processing data matrix: {str(e)}")
            raise