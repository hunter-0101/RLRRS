# IMPORTANT: This script requires the 'arxiv' library.
# You can install it using pip:
# pip install arxiv

import arxiv
import time
import sys

def search_arxiv_papers(query="large language models", max_results=5):
    """
    Searches the arXiv API for papers matching a query and prints their details.

    The client reuses connections and can be configured for stricter rate limits
    if you plan on heavy batch processing. The default is usually acceptable for
    small projects.

    Args:
        query (str): The search term to look for in the arXiv index.
        max_results (int): The maximum number of results to fetch and display.
    """
    print(f"--- Searching arXiv for: '{query}' (Max {max_results} results) ---")

    try:
        # 1. Create the API client
        # You can set custom delay_seconds here for strict adherence to the 
        # rate limit (e.g., delay_seconds=3.1) if you are making many sequential calls.
        client = arxiv.Client()

        # 2. Define the search criteria
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )

        # 3. Fetch and process the results
        # client.results returns a generator, which is memory efficient.
        results = client.results(search)
        
        found_count = 0
        for i, result in enumerate(results):
            found_count += 1
            print(f"\n[{i+1}] Title: {result.title.strip()}")
            print(f"    ID: {result.entry_id}")
            print(f"    Authors: {', '.join(a.name for a in result.authors)}")
            print(f"    Published: {result.published.strftime('%Y-%m-%d')}")
            # The summary is often very long, so we print a snippet
            print(f"    Summary Snippet: {result.summary.strip()[:200]}...")

        if found_count == 0:
            print("\nNo results found for this query.")
            
    except Exception as e:
        print(f"\n[ERROR] An error occurred during the API call: {e}", file=sys.stderr)
        print("Please ensure your internet connection is stable and the 'arxiv' library is installed.", file=sys.stderr)


if __name__ == "__main__":
    # Test the function with a common, recent topic
    search_arxiv_papers(query="Reinforcement Learning from Human Feedback")
    
    # Wait before making another query to respect the arXiv rate limit (1 request every 3 seconds)
    time.sleep(3) 

    # Another test to ensure the search functionality is versatile
    search_arxiv_papers(query="cat:cs.AI AND au:LeCun", max_results=2)