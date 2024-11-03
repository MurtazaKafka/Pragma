import re
from typing import List
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

class ContentCleaner:
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text content"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters while preserving necessary punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Normalize quotes and dashes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace('–', '-').replace('—', '-')
        
        return text.strip()

    @staticmethod
    def extract_relevant_sentences(text: str, keywords: List[str], context_window: int = 2) -> str:
        """Extract relevant sentences containing keywords with context"""
        sentences = sent_tokenize(text)
        relevant_indices = set()
        
        # Find sentences containing keywords
        for i, sentence in enumerate(sentences):
            if any(keyword.lower() in sentence.lower() for keyword in keywords):
                # Add context window
                for j in range(max(0, i - context_window), min(len(sentences), i + context_window + 1)):
                    relevant_indices.add(j)
        
        # Reconstruct text with relevant sentences
        relevant_sentences = [sentences[i] for i in sorted(relevant_indices)]
        return ' '.join(relevant_sentences)

    @staticmethod
    def clean_html(html_content: str) -> str:
        """Clean HTML content and extract readable text"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'meta', 'link', 'noscript']):
            element.decompose()
        
        # Extract text from remaining elements
        text = soup.get_text(separator=' ')
        return ContentCleaner.clean_text(text)