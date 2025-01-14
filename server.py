# server.py
from mcp.server.fastmcp import FastMCP, Image
import requests
from requests.structures import CaseInsensitiveDict
from urllib.parse import quote
import os
import generate_image
from PIL import Image as PILImage
import json
import subprocess

APIKEY = os.environ.get("GEO_APIKEY")
if APIKEY is None:
    raise ValueError("GEO_APIKEY environment variable is not set")

# Create an MCP server
mcp = FastMCP("Map Demo", dependencies=["requests", "pillow", "selenium", "folium"])

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

@mcp.tool()
def create_map_from_geojson(geojson_coordinates: dict) -> str:
    json.dump(geojson_coordinates, open("temp_geojson.json", "w"))
    subprocess.call(["uv", "run", "python", "generate_image.py", "temp_geojson.json"])
    subprocess.call(["open", "map.png"])
    return f"file lives at {os.curdir}/map.png"

if __name__ == "__main__":
    mcp.run() 