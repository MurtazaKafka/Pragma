from typing import List, Dict, Optional, Any
from openai import OpenAI
import asyncio
import json
import os
from datetime import datetime
from schemas import AnalysisResult, SearchResult
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

class LLMInterface:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.logger = logging.getLogger(__name__)
        
        # Configure default parameters
        self.default_model = "gpt-4"
        self.max_tokens = 1000
        self.temperature = 0.3
        
        # System prompts for different analysis types
        self.SYSTEM_PROMPTS = {
            'financial_analysis': """You are a financial analyst expert. Analyze the provided content and extract relevant financial information. 
            Focus on key metrics, trends, and important findings. Be precise and quantitative where possible.""",
            
            'risk_analysis': """You are a risk assessment expert. Analyze the provided content for potential risks and challenges. 
            Categorize risks by type (operational, financial, market, etc.) and assess their potential impact.""",
            
            'market_analysis': """You are a market research expert. Analyze the provided content for market trends, competitive positioning, 
            and industry dynamics. Focus on market share, growth opportunities, and competitive advantages."""
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def analyze_content(
        self,
        question: str,
        organization: str,
        search_results: List[SearchResult],
        analysis_type: str = 'financial_analysis'
    ) -> AnalysisResult:
        """Analyze content using GPT-4 with retry logic and structured output"""
        
        # Prepare context from search results
        context = self._prepare_context(search_results)
        
        # Construct the prompt
        system_prompt = self.SYSTEM_PROMPTS.get(analysis_type, self.SYSTEM_PROMPTS['financial_analysis'])
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": self._construct_analysis_prompt(
                question, organization, context
            )}
        ]

        try:
            # Make API call
            response = await self._make_api_call(messages)
            
            # Parse and validate response
            return self._parse_llm_response(response, search_results)
            
        except Exception as e:
            self.logger.error(f"Error in LLM analysis: {str(e)}")
            raise

    async def _make_api_call(self, messages: List[Dict[str, str]]) -> Dict:
        """Make the API call to OpenAI with proper error handling"""
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.default_model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            self.logger.error(f"OpenAI API call failed: {str(e)}")
            raise

    def _prepare_context(self, search_results: List[SearchResult]) -> str:
        """Prepare context from search results for the LLM"""
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"Source {i} ({result.url}):\n{result.content}\n")
        return "\n".join(context_parts)

    def _construct_analysis_prompt(self, question: str, organization: str, context: str) -> str:
        """Construct a detailed prompt for the LLM"""
        return f"""Analyze the following information about {organization} to answer the question: "{question}"

Context:
{context}

Please provide your analysis in the following JSON format:
{{
    "answer": "A comprehensive answer to the question",
    "key_findings": ["List of key findings"],
    "confidence_score": 0.0 to 1.0,
    "sources": ["List of relevant source URLs"],
    "relevant_quotes": ["Important quotes from the sources that support the findings"],
    "metadata": {{
        "analysis_timestamp": "current_timestamp",
        "data_timeframe": "time period covered by the analysis",
        "limitations": "any limitations in the analysis"
    }}
}}

Focus on providing accurate, well-supported conclusions based on the provided context."""

    def _parse_llm_response(self, response: Dict[str, Any], search_results: List[SearchResult]) -> AnalysisResult:
        """Parse and validate LLM response into AnalysisResult"""
        try:
            # Extract sources from search results
            sources = [result.url for result in search_results]
            
            return AnalysisResult(
                answer=response['answer'],
                key_findings=response['key_findings'],
                confidence_score=float(response['confidence_score']),
                sources=sources,
                relevant_quotes=response.get('relevant_quotes', []),
                metadata={
                    **response.get('metadata', {}),
                    'processed_timestamp': datetime.utcnow().isoformat()
                }
            )
        except KeyError as e:
            self.logger.error(f"Missing required field in LLM response: {str(e)}")
            raise ValueError(f"Invalid LLM response format: missing {str(e)}")
        except Exception as e:
            self.logger.error(f"Error parsing LLM response: {str(e)}")
            raise

    async def batch_analyze(
        self,
        questions: List[str],
        organizations: List[str],
        search_results: Dict[str, Dict[str, List[SearchResult]]]
    ) -> Dict[str, Dict[str, AnalysisResult]]:
        """Batch process multiple questions and organizations"""
        results = {}
        
        for question in questions:
            results[question] = {}
            for org in organizations:
                try:
                    org_results = search_results.get(question, {}).get(org, [])
                    if org_results:
                        results[question][org] = await self.analyze_content(
                            question=question,
                            organization=org,
                            search_results=org_results
                        )
                    else:
                        self.logger.warning(f"No search results found for {question} - {org}")
                except Exception as e:
                    self.logger.error(f"Error analyzing {question} for {org}: {str(e)}")
                    results[question][org] = None
                
                # Add delay between requests to avoid rate limiting
                await asyncio.sleep(0.5)
        
        return results

# Example usage in RAGProcessor
async def process_queries(self, questions: List[str], organizations: List[str]) -> QueryResponse:
    llm = LLMInterface()
    results = await llm.batch_analyze(questions, organizations, search_results)
    return QueryResponse(
        request_id=str(uuid.uuid4()),
        results=results,
        processing_time=time.time() - start_time,
        total_sources_analyzed=len(search_results)
    )