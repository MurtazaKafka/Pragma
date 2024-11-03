import asyncio
import aiohttp
import json

async def test_analysis():
    # Test data
    test_request = {
        "questions": [
            "What was the revenue growth?",
            "What is the profit margin?"
        ],
        "organizations": [
            "Apple Inc",
            "Microsoft"
        ]
    }
    
    print("\nSending request to analyze data...")
    
    # Make request to local API
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://localhost:8000/api/analyze',
            json=test_request
        ) as response:
            result = await response.json()
            
            # Print results
            print("\nAPI Response:")
            print(f"Status: {result['status']}")
            print("\nCSV Data:")
            print(result['data'])
            
            # Optionally save CSV to file
            if result['status'] == 'success':
                with open('analysis_results.csv', 'w') as f:
                    f.write(result['data'])
                print("\nResults have been saved to 'analysis_results.csv'")

if __name__ == "__main__":
    try:
        asyncio.run(test_analysis())
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        
        # Additional error handling for common issues
        if isinstance(e, aiohttp.ClientConnectorError):
            print("\nCouldn't connect to the server. Make sure the FastAPI server is running (uvicorn backend.endpoints:app --reload)")
        elif isinstance(e, aiohttp.ClientError):
            print("\nAPI request failed. Check if the server is functioning properly.")
        elif isinstance(e, KeyError):
            print("\nUnexpected response format from the API.")