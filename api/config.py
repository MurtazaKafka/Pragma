import os
from typing import Dict
from dotenv import load_dotenv
from pathlib import Path

class Config:
    """Configuration handler for API keys and environment variables"""
    
    REQUIRED_VARS = {
        'OPENAI_API_KEY': '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',
        'PINECONE_API_KEY': 'ab29b834-62bc-4b89-8586-6ec0868dae44',
        'PINECONE_ENV': 'c2i',
        'PINECONE_INDEX_NAME': 'us-west1-gcp-free'
    }

    @staticmethod
    def load_environment():
        """Load environment variables from .env file and validate them"""
        # Try to load from .env file
        env_path = Path('.env')
        if env_path.exists():
            load_dotenv(env_path)
        
        # Validate required environment variables
        missing_vars = []
        for var, description in Config.REQUIRED_VARS.items():
            if not os.getenv(var):
                missing_vars.append(f"- {var}: {description}")


    @staticmethod
    def get_api_keys() -> Dict[str, str]:
        """Get all API keys after validating their presence"""
        Config.load_environment()
        return {
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'pinecone_api_key': os.getenv('PINECONE_API_KEY'),
            'pinecone_env': os.getenv('PINECONE_ENV'),
            'pinecone_index_name': os.getenv('PINECONE_INDEX_NAME')
        }