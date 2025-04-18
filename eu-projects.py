import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point, LineString

# Load world map data
#world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = gpd.read_file("data/ne_50m_admin_0_countries.shp")

# Define a bounding box for Europe in EPSG:4326 (lon/lat)
europe_bounds = {
    "minx": -25,   # westernmost (e.g., Portugal/Iceland)
    "maxx": 45,    # easternmost (e.g., Slovakia/Ukraine)
    "miny": 34,    # southernmost (e.g., Mediterranean)
    "maxy": 72     # northernmost (e.g., Scandinavia)
}

# Keep only countries within the bounding box
world_europe = world.cx[
    europe_bounds["minx"]:europe_bounds["maxx"],
    europe_bounds["miny"]:europe_bounds["maxy"]
]

# Then reproject as needed
world_europe = world_europe.to_crs(epsg=3857)

# Filter for countries you want to show (e.g., in Europe)
countries = world[world['NAME'].isin(['Spain', 'Germany', 'France', 
                                      'Italy', 'Belgium', 'Netherlands', 
                                      'Poland', 'Portugal', 'Slovakia',
                                      'Ireland', 'Turkey', 'Denmark',
                                      'Norway', 'Sweden', 'United Kingdom'])]

#import folium
#
## Create a map centered on a location (example: Europe)
#m = folium.Map(location=[52.5200, 13.4050], zoom_start=6)
#
## Add OpenStreetMap tiles (you can use CartoDB as well)
#folium.TileLayer('CartoDB positron').add_to(m)
#
## Save to HTML and view in the browser (vector tiles for sharpness)
#m.save("high_res_map.html")

# Define Karlsruhe (the hub)
karlsruhe_coords = (8.4037, 49.0069)  # lon, lat

# Define AI4EOSC destination cities
ai4eosc = {
    'destinations': { 'Valencia': (-0.3763, 39.4699),
                      'Santander': (-3.8044, 43.4623),
                      'Lisboa': (-9.1393, 38.7223),
                      'Bologne': (11.3426, 44.4949),
                      'Poznan': (16.9252, 52.4064),
                      'Bratislava': (17.1077, 48.1486)
                    },
    'line':   { 'color': 'darkcyan',
                'width': 1.2,
                'style': '-',
                'alpha': 0.5
              },
    'marker': { 'color': 'deeppink',
                'size': 2,
                'style': '*',
                'alpha': 0.5
              },
}

# Define iMagine-AI destination cities
shift_same_city=0.3
imagine_ai = {
    'destinations': { 'Valencia': (-0.3763, 39.4699+shift_same_city),
                      'Santander': (-3.8044, 43.4623+shift_same_city),
                      'Lisboa': (-9.1393, 38.7223+shift_same_city),
                      'Bratislava': (17.1077, 48.1486+shift_same_city)
                    },
    'line':   { 'color': 'darkblue',
                'width': 1.2,
                'style': '-',
                'alpha': 0.5
              },
    'marker': { 'color': 'orange',
                'size': 2,
                'style': '*',
                'alpha': 0.5
              },
}


# Create GeoDataFrame for cities
def city_geo(destinations):
    city_data = {
        'name': ['Karlsruhe'] + list(destinations.keys()),
        'lon': [karlsruhe_coords[0]] + [lon for lon, lat in destinations.values()],
        'lat': [karlsruhe_coords[1]] + [lat for lon, lat in destinations.values()],
    }
    city_gdf = gpd.GeoDataFrame(
        city_data,
        geometry=[Point(xy) for xy in zip(city_data['lon'], city_data['lat'])],
        crs="EPSG:4326"
    )
    return city_gdf

# Create lines from Karlsruhe to each destination
def lines_geo(destinations):
    lines = [
        LineString([Point(karlsruhe_coords), Point(coord)])
        for coord in destinations.values()
    ]
    line_gdf = gpd.GeoDataFrame(geometry=lines, crs="EPSG:4326")
    return line_gdf

# Function to draw lines
def draw_connections(project):
    city_gdf = city_geo(project['destinations'])
    line_gdf = lines_geo(project['destinations'])
    city_gdf = city_gdf.to_crs(epsg=3857)
    line_gdf = line_gdf.to_crs(epsg=3857)

    line = project['line']
    # Plot lines
    line_gdf.plot(ax=ax, color=line['color'], linewidth=line['width'], linestyle=line['style'], zorder=2, alpha=line['alpha'])
    # Plot cities
    marker = project['marker']
    city_gdf.plot(ax=ax, color=marker['color'], markersize=marker['size'], zorder=3, alpha=marker['alpha'])



# Reproject all to Web Mercator for contextily
countries = countries.to_crs(epsg=3857)
# Reproject only Europe as needed
world_europe = world_europe.to_crs(epsg=3857)

# Plotting
fig, ax = plt.subplots(figsize=(12, 12), dpi=200) # Bigger figure and higher DPI

# Select Spain from the countries GeoDataFrame
# Fill Spain with semi-transparent dark cyan
#spain = world[world['NAME'] == 'Spain'].to_crs(epsg=3857)
#spain.plot(ax=ax, color='darkcyan', alpha=0.5, edgecolor='darkcyan')

# Draw country boundaries
#countries.boundary.plot(ax=ax, color='darkcyan')
countries.boundary.plot(ax=ax, color='dimgray', linewidth=0.5, linestyle='--', antialiased=True, alpha=0.5)

draw_connections(imagine_ai)
draw_connections(ai4eosc)

# Plot city names (we combine cities from all projects, because there can be duplicates otherwise)
cities = {  **ai4eosc['destinations'],
            **imagine_ai['destinations']
         }
print(cities)
cities_gdf = city_geo(cities)
cities_gdf = cities_gdf.to_crs(epsg=3857)
for x, y, label in zip(cities_gdf.geometry.x, cities_gdf.geometry.y, cities_gdf['name']):
    ax.text(x + 10000, y + 10000, label, fontsize=4)

#for x, y, label in zip(city_gdf.geometry.x, city_gdf.geometry.y, city_gdf['name']):
#    ax.text(x + 5000, y + 5000, label, fontsize=12, fontweight='bold', 
#            ha='center', va='center', color='black', 
#            bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle="round,pad=0.3"))

# Add OpenStreetMap basemap at a higher zoom level
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=5)
#ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=4)

plt.title("EU projects connections")
plt.axis('off')
plt.tight_layout()
plt.savefig("map_high_res.pdf", dpi=600, bbox_inches='tight')  # 300+ DPI = print quality
plt.show()
