from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
from scraper import WebScraper
from rag_processor import EnhancedRAGProcessor
from schemas import QueryRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/api/analyze")
async def analyze_data(request: QueryRequest):
    try:
        # Validate input
        if not request.questions or not request.organizations:
            raise HTTPException(
                status_code=400,
                detail="Both questions and organizations must be provided"
            )
            
        logger.info(f"Processing request with {len(request.questions)} questions and {len(request.organizations)} organizations")
        
        # Initialize services
        scraper = WebScraper()
        rag = EnhancedRAGProcessor()
        
        # Get search results
        try:
            search_results = await scraper.scrape_matrix(
                request.questions,
                request.organizations
            )
            logger.info(f"Successfully scraped {len(search_results)} results")
            
        except Exception as e:
            logger.error(f"Scraping error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error during web scraping: {str(e)}"
            )
        
        # Process with RAG
        try:
            results_df = await rag.process_data_matrix(
                request.questions,
                request.organizations,
                search_results  # Pass the search_results here
            )
            logger.info("Successfully processed data with RAG")
            
        except Exception as e:
            logger.error(f"RAG processing error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error during RAG processing: {str(e)}"
            )
        
        # Convert to CSV
        try:
            csv_data = results_df.to_csv(index=False)
            return {
                "status": "success",
                "data": csv_data
            }
            
        except Exception as e:
            logger.error(f"CSV conversion error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error converting results to CSV: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )