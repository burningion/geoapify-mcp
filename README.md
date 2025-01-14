# Geoapify MCP Server

Convert addresses into GPS coordinates for mapping, and optionally create an image of those coordinates using the Geoapify server.

![Example Map](./temp_map.png)

## Installation

You'll need to get an API key from [Geoapify](https://www.geoapify.com/), and set it as an environment variable named `GEO_APIKEY`.

Your `claude_desktop_config.json` will look like this after:

```json
"MCP Map Demo": {
      "command": "uv",
      "args": [
	"--directory",
        "/PATH/TO/THIS/REPO",
        "run",
        "--with",
        "fastmcp",
        "--with",
        "requests",
        "--with",
        "folio",
        "--with",
        "selenium",
        "--with",
        "pillow",
        "fastmcp",
        "run",
        "/PATH/TO/THIS/REPO/server.py"
      ],
      "env": {
        "GEO_APIKEY": "YOURAPIKEY"
      }
    }
```

You'll notice we include all the dependencies in our `args`.

## Tools

`get_gps_coordinates`

Used to get GPS coordinates from the API for creating GEOJSON, etc.

`create_map_from_geojson`

Create a map image and show it. (Showing only works on MacOS for now.)


## Example Usage

**Get GPS Coordinates** 

```
can you create a geojson of the following locations including their gps coordinates: 179 avenue du Général Leclerc, côté Rive Gauche
158 avenue du Général Leclerc, côté Rive Droite à l'angle de la rue Jules Herbron
112 avenue du Général Leclerc, côté Rive Droite
34 avenue du Général Leclerc, côté Rive Droite
En face du 57 rue Gaston Boissier, à côté de la borne
Route du Pavé de Meudon - à côté du chêne de la Vierge
6 avenue de Versailles (près du centre aquatique des Bertisettes)
3 places sur parking de la rue Costes et Bellonte
Rue Joseph Chaleil
18 rue des Sables – à côté de la crèche
25 sente de la Procession
33 rue Joseph Bertrand
Place Saint Paul
Place de la bataille de Stalingrad
Placette croisement avenue Pierre Grenier / avenue Robert Hardouin
107 avenue Gaston Boissier (en face de la caserne des pompiers)
```

**Result:** [Attached JSON file](./geo.json)

Returns a GeoJSON file.

**Create a Map Image**

```
can you create a map from my attached geojson file?
```
[Attached JSON file](./geo.json)

**Result:** ![temp map](./temp_map.png)

## LICENSE

MIT
