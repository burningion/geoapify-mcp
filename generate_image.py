import folium
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import sys


import logging

logging.basicConfig(
    filename='generator.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_map_from_geojson(geojson_data, output_file="map.png", zoom_start=15):
    # Calculate the center point for the map
    coordinates = []
    for feature in geojson_data['features']:
        lon, lat = feature['geometry']['coordinates']
        coordinates.append([lat, lon])  # Folium uses lat, lon order
    
    center_lat = sum(coord[0] for coord in coordinates) / len(coordinates)
    center_lon = sum(coord[1] for coord in coordinates) / len(coordinates)
    
    # Create a map centered on the middle point
    m = folium.Map(location=[center_lat, center_lon], 
                  zoom_start=zoom_start,
                  tiles='OpenStreetMap')
    
    # Add markers for each location
    for feature in geojson_data['features']:
        lon, lat = feature['geometry']['coordinates']
        name = feature['properties'].get('name', 'Unnamed Location')
        description = feature['properties'].get('description', '')
        
        popup_text = f"{name}<br>{description}" if description else name
        
        folium.Marker(
            [lat, lon],  # Folium uses lat, lon order
            popup=popup_text,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    
    # Save as HTML first
    html_file = "temp_map.html"
    m.save(html_file)
    
    # Set up Chrome options for headless rendering
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1024,768")
    
    # Initialize webdriver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Load the HTML file
    driver.get(f"file://{os.path.abspath(html_file)}")
    
    # Wait for tiles to load
    time.sleep(2)
    
    # Take screenshot
    driver.save_screenshot(output_file)
    
    # Clean up
    driver.quit()
    os.remove(html_file)
    
    return output_file

# Example usage
if __name__ == "__main__":
    # Check if filename was provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <geojson_file>")
        sys.exit(1)
    
    # Read GeoJSON from file
    try:
        with open(sys.argv[1], 'r') as f:
            geojson_data = json.load(f)
            
        # Create the map
        output_file = create_map_from_geojson(geojson_data)
        print(f"Map has been saved as {output_file}")
        
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{sys.argv[1]}' is not valid JSON")
        sys.exit(1)
