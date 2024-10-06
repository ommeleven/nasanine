import requests
import folium
import folium.plugins
from folium import Map, TileLayer 
from pystac_client import Client 
import branca 
import pandas as pd
import matplotlib.pyplot as plt

# Provide STAC and RASTER API endpoints
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

# Please use the collection name similar to the one used in the STAC collection.
# Name of the collection for CASA GFED Land-Atmosphere Carbon Flux monthly emissions. 
collection_name = "casagfed-carbonflux-monthgrid-v3"
# Fetch the collection from STAC collections using the appropriate endpoint
# the 'requests' library allows a HTTP request possible
collection = requests.get(f"{STAC_API_URL}/collections/{collection_name}").json()
#print(collection)
# Create a function that would search for the above data collection in the STAC API
def get_item_count(collection_id):
    count = 0
    items_url = f"{STAC_API_URL}/collections/{collection_id}/items"

    while True:
        response = requests.get(items_url)

        if not response.ok:
            print("error getting items")
            exit()

        stac = response.json()
        count += int(stac["context"].get("returned", 0))
        next = [link for link in stac["links"] if link["rel"] == "next"]

        if not next:
            break
        items_url = next[0]["href"]

    return count

# Apply the above function and check the total number of items available within the collection
number_of_items = get_item_count(collection_name)
items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]
#print(f"Found {len(items)} items")
# Examine the first item in the collection
#print(items[0])
# To access the year value from each item more easily, this will let us query more explicitly by year and month (e.g., 2020-02)
items = {item["properties"]["start_datetime"][:7]: item for item in items} 
# rh = Heterotrophic Respiration
asset_name = "rh"
rescale_values = {"max":items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"], "min":items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]}
color_map = "purd" # please refer to matplotlib library if you'd prefer choosing a different color ramp.
# For more information on Colormaps in Matplotlib, please visit https://matplotlib.org/stable/users/explain/colors/colormaps.html

# To change the year and month of the observed parameter, you can modify the "items['YYYY-MM']" statement
# For example, you can change the current statement "items['2003-12']" to "items['2016-10']" 
december_2003_tile = requests.get(
    f"{RASTER_API_URL}/collections/{items['2003-12']['collection']}/items/{items['2003-12']['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}", 
).json()
# Now we apply the same process used in the previous step for the December 2017 tile
december_2017_tile = requests.get(
    f"{RASTER_API_URL}/collections/{items['2017-12']['collection']}/items/{items['2017-12']['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}", 
).json()

# For this study we are going to compare the RH level in 2003 and 2017 over the State of Texas 
# To change the location, you can simply insert the latitude and longitude of the area of your interest in the "location=(LAT, LONG)" statement
# For example, you can change the current statement "location=(31.9, -99.9)" to "location=(34, -118)" to monitor the RH level in California instead of Texas

# Set initial zoom and center of map for CO₂ Layer
# 'folium.plugins' allows mapping side-by-side
map_ = folium.plugins.DualMap(location=(34, -118), zoom_start=6)

# The TileLayer library helps in manipulating and displaying raster layers on a map
# December 2003
'''map_layer_2003 = TileLayer(
    tiles=december_2003_tile["tiles"][0],
    attr="GHG",
    opacity=0.8,
    name="December 2003 RH Level",
    overlay= True,
    legendEnabled = True
)
map_layer_2003.add_to(map_.m1)
'''

# December 2017
map_layer_2017 = TileLayer(
    tiles=december_2017_tile["tiles"][0],
    attr="GHG",
    opacity=0.8,
    name="December 2017 RH Level",
    overlay= True,
    legendEnabled = True
)
map_layer_2017.add_to(map_.m1)


# Display data markers (titles) on both maps
folium.Marker((40, 5.0), tooltip="both").add_to(map_)
folium.LayerControl(collapsed=False).add_to(map_)


# Add a legend to the dual map using the 'branca' library. 
# Note: the inserted legend is representing the minimum and maximum values for both tiles.
colormap = branca.colormap.linear.PuRd_09.scale(0, 0.3) # minimum value = 0, maximum value = 0.3 (kg Carbon/m2/month)
colormap = colormap.to_step(index=[0, 0.07, 0.15, 0.22, 0.3])
colormap.caption = 'Rh Values (kg Carbon/m2/month)'

colormap.add_to(map_.m1)


# Visualizing the map
map_.save('STAC_map.html')