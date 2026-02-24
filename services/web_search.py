"""
Web search service for Court Herald and Royal Envoy.
Uses Tavily API for real-time web search capabilities.
"""

import os
import httpx
from typing import List, Dict

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")


async def web_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Perform a web search using Tavily API.
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
    
    Returns:
        List of search results with title, url, and content
    """
    if not TAVILY_API_KEY:
        return [{
            "title": "Web search not configured",
            "url": "",
            "content": "TAVILY_API_KEY environment variable not set. Web search is disabled."
        }]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "max_results": max_results,
                    "search_depth": "basic",
                    "include_answer": True,
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                # Add the AI-generated answer if available
                if data.get("answer"):
                    results.append({
                        "title": "Summary",
                        "url": "",
                        "content": data["answer"]
                    })
                
                # Add search results
                for result in data.get("results", []):
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": result.get("content", "")
                    })
                
                return results
            else:
                return [{
                    "title": "Search failed",
                    "url": "",
                    "content": f"Web search API returned status code {response.status_code}"
                }]
    
    except Exception as e:
        return [{
            "title": "Search error",
            "url": "",
            "content": f"Web search failed: {str(e)}"
        }]


def format_search_results(results: List[Dict[str, str]]) -> str:
    """Format search results into a readable string for LLM context."""
    if not results:
        return "No search results found."
    
    formatted = "Web search results:\n\n"
    for i, result in enumerate(results, 1):
        formatted += f"{i}. {result['title']}\n"
        if result['url']:
            formatted += f"   URL: {result['url']}\n"
        formatted += f"   {result['content']}\n\n"
    
    return formatted
