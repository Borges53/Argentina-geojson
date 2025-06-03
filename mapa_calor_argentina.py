# filepath: c:\Argentina-geojson\mapa_calor_argentina.py
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Load the Argentina GeoJSON
geojson_path = 'argentina.geojson'
gdf = gpd.read_file(geojson_path)

# Example values for each province (you can modify this data)
values = {
    'Buenos Aires': 100,
    'Catamarca': 20,
    'Chaco': 50,
    'Chubut': 30,
    'Cordoba': 80,
    'Corrientes': 40,
    'Entre Rios': 60,
    'Formosa': 10,
    'Jujuy': 25,
    'La Pampa': 15,
    'La Rioja': 18,
    'Mendoza': 70,
    'Misiones': 35,
    'Neuquen': 22,
    'Rio Negro': 28,
    'Salta': 55,
    'San Juan': 32,
    'San Luis': 17,
    'Santa Cruz': 12,
    'Santa Fe': 90,
    'Santiago del Estero': 27,
    'Tierra del Fuego': 8,
    'Tucuman': 65
}

# Create a DataFrame with the values
values_df = pd.DataFrame(list(values.items()), columns=['name', 'value'])

# Merge the values into the GeoDataFrame
# If the 'name' column does not exist, try to extract it from 'properties'
if 'name' not in gdf.columns:
    if 'properties' in gdf.columns:
        gdf['name'] = gdf['properties'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
    elif 'properties.name' in gdf.columns:
        gdf['name'] = gdf['properties.name']
    else:
        print('Available columns in the GeoDataFrame:', gdf.columns)
        raise KeyError('The "name" column was not found in the GeoDataFrame')

mapa = gdf.merge(values_df, left_on='name', right_on='name')

# Plot the heatmap
fig, ax = plt.subplots(1, 1, figsize=(10, 12))
mapa.plot(column='value', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
ax.set_title('Argentina Provinces Heatmap', fontsize=16)
ax.axis('off')

# Add province names at the centroid of each polygon
for idx, row in mapa.iterrows():
    if row['geometry'].geom_type == 'Polygon' or row['geometry'].geom_type == 'MultiPolygon':
        x, y = row['geometry'].centroid.x, row['geometry'].centroid.y
        ax.text(x, y, row['name'], fontsize=8, ha='center', va='center', color='black', weight='bold',
                bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

plt.show()
