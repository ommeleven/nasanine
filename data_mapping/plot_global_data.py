'''
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Define the path to the GeoTIFF file (Heterotrophic Respiration (Rh) in this case)
file_path = 'path/to/your/GEOSCarb_CASAGFED3v3_Rh_Flux_Monthly_x720_y360_201712.tif'

# Open the GeoTIFF file
with rasterio.open(file_path) as src:
    # Read the data
    rh_data = src.read(1)  # Reading the first (and only) band
    rh_data = np.where(rh_data == src.nodata, np.nan, rh_data)  # Handle nodata values

    # Get the bounding box and the transform
    bbox = src.bounds
    transform = src.transform

# Set up the plot
fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_title('Global Heterotrophic Respiration (Rh) - December 2017')

# Plot the raster data
extent = [bbox.left, bbox.right, bbox.bottom, bbox.top]
ax.imshow(rh_data, origin='upper', extent=extent, transform=ccrs.PlateCarree(), cmap='viridis')

# Add coastlines and gridlines for reference
ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# Add some land and ocean features for better visualization
ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')
ax.add_feature(cfeature.OCEAN, zorder=0)

# Show the plot
plt.colorbar(ax.images[0], ax=ax, orientation='vertical', label='Heterotrophic Respiration (Rh) Flux')
plt.show()

'''
import matplotlib.pyplot as plt
import numpy as np

# Data extracted from the provided JSON
assets = {
    'rh': {'mean': 0.006758838426321745, 'title': 'Heterotrophic Respiration (Rh)'},
    'nee': {'mean': 0.0015448036137968302, 'title': 'Net Ecosystem Exchange (NEE)'},
    'npp': {'mean': 0.005214035045355558, 'title': 'Net Primary Production (NPP)'},
    'fire': {'mean': 0.00025634843041189015, 'title': 'Fire Emissions (FIRE)'},
    'fuel': {'mean': 5.057307134848088e-05, 'title': 'Wood Fuel Emissions (FUEL)'}
}

# Prepare data for plotting
labels = [assets[key]['title'] for key in assets]
means = [assets[key]['mean'] for key in assets]

# Create bar plot
plt.figure(figsize=(12, 6))
bars = plt.bar(labels, means)

# Customize the plot
plt.title('Mean Carbon Flux by Asset (December 2017)', fontsize=16)
plt.xlabel('Asset', fontsize=12)
plt.ylabel('Mean Flux', fontsize=12)
plt.xticks(rotation=45, ha='right')

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2e}',
             ha='center', va='bottom')

# Adjust layout and display the plot
plt.tight_layout()
plt.show()