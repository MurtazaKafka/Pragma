from typing import List, Dict, Optional
import os
from dataclasses import dataclass
import json
import pandas as pd
from openai import OpenAI
from pinecone import Pinecone
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from config import Config

logger = logging.getLogger(__name__)

@dataclass
class EnhancedSearchResult:
    question: str
    organization: str
    content: str
    url: str
    timestamp: datetime = datetime.now()
    content_type: str = "webpage"
    relevance_score: float = 0.5

class EnhancedRAGProcessor:
    def __init__(self):
        try:
            # Load and validate all required API keys
            api_keys = Config.get_api_keys()
            
            # Initialize OpenAI client
            self.openai_client = OpenAI(
                api_key=api_keys['openai_api_key']
            )
            
            # Initialize Pinecone
            self.pc = Pinecone(
                api_key=api_keys['pinecone_api_key'],
                environment=api_keys['pinecone_env']
            )
            
            # Get or create Pinecone index
            index_name = api_keys['pinecone_index_name']
            try:
                self.index = self.pc.Index(index_name)
            except Exception as e:
                logger.warning(f"Error accessing index: {str(e)}")
                logger.info("Attempting to create new index...")
                self.pc.create_index(
                    name=index_name,
                    dimension=1536,  # dimension for text-embedding-ada-002
                    metric="cosine"
                )
                self.index = self.pc.Index(index_name)
                
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            raise

        # Define enhanced prompts
        self.ANALYSIS_PROMPT_TEMPLATE = """
        Analyze the following sources to answer the question: "{question}" about {organization}.
        
        Sources:
        {sources}
        
        Focus on extracting:
        1. Specific numerical data and metrics
        2. Time periods and trends
        3. Comparative analysis
        4. Source reliability
        
        Requirements:
        - Provide detailed quantitative analysis where available
        - Include specific dates and time periods
        - Compare against industry benchmarks if mentioned
        - Cite specific sources for each key finding
        
        Respond in the following JSON format:
        {{
            "answer": "Comprehensive answer with specific numbers and dates",
            "key_findings": [
                "Specific finding 1 with numbers and dates",
                "Specific finding 2 with numbers and dates",
                ...
            ],
            "metrics": {{
                "value": numeric_value,
                "unit": "percentage/currency/etc",
                "time_period": "Q1 2024/FY2023/etc",
                "trend": "increasing/decreasing/stable"
            }},
            "confidence_score": 0.0 to 1.0,
            "reliability_assessment": {{
                "source_quality": 0.0 to 1.0,
                "data_recency": "date of most recent data",
                "data_completeness": 0.0 to 1.0
            }},
            "sources": ["url1", "url2", ...]
        }}
        """

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _get_embedding(self, text: str) -> List[float]:
        """Get embedding with retry logic"""
        response = self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding

    async def vectorize_content(self, search_results: List[EnhancedSearchResult]) -> List[Dict]:
        """Enhanced vectorization with metadata"""
        vectors = []
        
        for result in search_results:
            try:
                # Prepare content with metadata
                content_with_metadata = f"""
                Organization: {result.organization}
                Question Context: {result.question}
                Content Type: {result.content_type}
                Timestamp: {result.timestamp}
                Content: {result.content[:8000]}
                """
                
                embedding = await self._get_embedding(content_with_metadata)
                
                # Create unique ID
                unique_id = f"{hash(result.question + result.organization + str(result.url))}"
                
                # Enhanced metadata
                metadata = {
                    "question": result.question,
                    "organization": result.organization,
                    "content": result.content[:8000],
                    "url": str(result.url),
                    "timestamp": result.timestamp.isoformat(),
                    "content_type": result.content_type or 'webpage',
                    "relevance_score": float(result.relevance_score or 0.5)  # Ensure float and non-null
                }
                
                vectors.append({
                    "id": unique_id,
                    "values": embedding,
                    "metadata": metadata
                })
                
            except Exception as e:
                print(f"Error vectorizing content: {str(e)}")
                continue
        
        return vectors

    async def query_vector_db(self, question: str, organization: str, top_k: int = 5) -> List[Dict]:
        """Enhanced vector DB querying"""
        try:
            query_text = f"Question about {organization}: {question}"
            query_embedding = await self._get_embedding(query_text)
            
            # Enhanced query with metadata filtering and scoring
            results = self.index.query(
                vector=query_embedding,
                filter={
                    "organization": {"$eq": organization},
                    "relevance_score": {"$gte": 0.5}  # Filter for relevant content
                },
                top_k=top_k,
                include_metadata=True
            )
            
            # Sort results by relevance and recency
            sorted_results = sorted(
                results.matches,
                key=lambda x: (
                    x.score,  # Vector similarity
                    x.metadata.get('relevance_score', 0),  # Content relevance
                    x.metadata.get('timestamp', '2000-01-01')  # Recency
                ),
                reverse=True
            )
            
            return sorted_results
            
        except Exception as e:
            print(f"Error querying vector database: {str(e)}")
            return []

    async def process_with_llm(
        self,
        query_results: List[Dict],
        question: str,
        organization: str
    ) -> Dict:
        """Enhanced LLM processing"""
        try:
            # Prepare sources with metadata
            sources_text = "\n\n".join([
                f"Source {i+1} ({result.metadata.get('content_type', 'unknown')}, "
                f"{result.metadata.get('timestamp', 'unknown date')}):\n"
                f"{result.metadata['content']}"
                for i, result in enumerate(query_results)
            ])
            
            # Construct prompt with enhanced template
            prompt = self.ANALYSIS_PROMPT_TEMPLATE.format(
                question=question,
                organization=organization,
                sources=sources_text
            )
            
            # Get LLM response with structured output format
            response = self.openai_client.chat.completions.create(
                model="gpt-4-1106-preview",  # Use a model that supports JSON output
                messages=[
                    {"role": "system", "content": "You are a financial analysis expert. Always respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}  # This will work with gpt-4-1106-preview
            )
            
            # Parse the response
            try:
                result = json.loads(response.choices[0].message.content)
                return result
            except json.JSONDecodeError:
                # Fallback for non-JSON responses
                return {
                    "answer": "Error: Invalid response format",
                    "key_findings": [],
                    "metrics": {},
                    "confidence_score": 0.0,
                    "reliability_assessment": {
                        "source_quality": 0.0,
                        "data_recency": "unknown",
                        "data_completeness": 0.0
                    },
                    "sources": []
                }
                
        except Exception as e:
            print(f"Error processing with LLM: {str(e)}")
            raise

    async def process_data_matrix(
        self,
        questions: List[str],
        organizations: List[str],
        search_results: List[EnhancedSearchResult]
    ) -> pd.DataFrame:
        """Enhanced matrix processing"""
        try:
            # Vectorize and store results
            vectors = await self.vectorize_content(search_results)
            if vectors:
                self.index.upsert(vectors=vectors)
            
            # Process each pair with enhanced error handling
            results = []
            for question in questions:
                for org in organizations:
                    try:
                        # Query vector DB
                        relevant_content = await self.query_vector_db(question, org)
                        
                        if not relevant_content:
                            raise ValueError(f"No relevant content found for {org} - {question}")
                        
                        # Process with LLM
                        processed_result = await self.process_with_llm(
                            relevant_content,
                            question,
                            org
                        )
                        
                        # Create detailed row
                        row = {
                            'Question': question,
                            'Organization': org,
                            'Answer': processed_result['answer'],
                            'Key Findings': '; '.join(processed_result['key_findings']),
                            'Metrics': json.dumps(processed_result['metrics']),
                            'Confidence': processed_result['confidence_score'],
                            'Source Quality': processed_result['reliability_assessment']['source_quality'],
                            'Data Recency': processed_result['reliability_assessment']['data_recency'],
                            'Data Completeness': processed_result['reliability_assessment']['data_completeness'],
                            'Sources': '; '.join(processed_result['sources'])
                        }
                        
                        results.append(row)
                        
                    except Exception as e:
                        # Add error row with details
                        results.append({
                            'Question': question,
                            'Organization': org,
                            'Answer': f"Error: {str(e)}",
                            'Key Findings': '',
                            'Metrics': '{}',
                            'Confidence': 0.0,
                            'Source Quality': 0.0,
                            'Data Recency': 'unknown',
                            'Data Completeness': 0.0,
                            'Sources': ''
                        })
            
            return pd.DataFrame(results)
            
        except Exception as e:
            print(f"Error processing data matrix: {str(e)}")
            raise