import pandas as pd
import folium

# Load the data
data = pd.DataFrame({
    'site_code': ['ACT', 'ACT', 'ACT', 'ACT'],  # extend this list with all site_codes
    'latitude': [36.5332, 36.3336, 36.4011, 36.4645],  # all latitudes
    'longitude': [-76.9117, -77.1419, -77.0741, -77.4188],  # all longitudes
    'elevation': [5599.0, 333.0, 949.0, 3341.0]  # all elevations
})

# Create a base map
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=6)

# Add points to the map
for _, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Site: {row['site_code']}\nElevation: {row['elevation']}m",
    ).add_to(m)

# Save the map to an HTML file
m.save("map.html")
