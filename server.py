# server.py
from mcp.server.fastmcp import FastMCP
import requests
from requests.structures import CaseInsensitiveDict
from urllib.parse import quote
import os

APIKEY = os.environ.get("GEO_APIKEY")
if APIKEY is None:
    raise ValueError("GEO_APIKEY environment variable is not set")

# Create an MCP server
mcp = FastMCP("Map Demo", dependencies=["requests"])

def get_geocode(search_address, api_key):
    # URL encode the address to handle special characters
    encoded_address = quote(search_address)
    
    url = f"https://api.geoapify.com/v1/geocode/search?text={encoded_address}&apiKey={api_key}"
    
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    
    resp = requests.get(url, headers=headers)
    return resp.json()

# Get GPS coordinates for an address
@mcp.tool()
def get_gps_coordinates(address: str) -> dict:
    """Add two numbers"""
    return get_geocode(address, APIKEY)


if __name__ == "__main__":
    mcp.run() 