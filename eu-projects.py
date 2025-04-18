import geopandas as gpd
import logging
import matplotlib.pyplot as plt
import contextily as ctx
from iteration_utilities import duplicates
from shapely.geometry import Point, LineString, box

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # 0: Not set, 10: DEBUG, 20: INFO, 30: WARNING, 40: ERROR, 50: CRITICAL

# create console handler and set level to debug
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#logger.addHandler(ch)

# Load world map data
world = gpd.read_file("data/ne_50m_admin_0_countries.shp")
# how detailed map to save, larger number - more details
basemap_zoom = 7
# size of the city marker
marker_size = 3

# how much shift lat for repeated cities
lat_shift = 0.1


# Define a bounding box for Europe in EPSG:4326 (lon/lat)
#  "minx": -25,   # westernmost (e.g., Portugal/Iceland)
#  "maxx": 45,    # easternmost (e.g., Slovakia/Ukraine)
#  "miny": 34,    # southernmost (e.g., Mediterranean)
#  "maxy": 72     # northernmost (e.g., Scandinavia)
#  box(minx, miny, maxx, maxy)
europe_bbox = box(-25, 32, 40, 60)

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
    'name': 'AI4EOSC',
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
                'size': marker_size,
                'style': '*',
                'alpha': 0.5
              },
}

# Define iMagine-AI destination cities
imagine_ai = {
    'name': 'iMagine',
    'destinations': { 'Valencia': (-0.3763, 39.4699),
                      'Santander': (-3.8044, 43.4623),
                      'Lisboa': (-9.1393, 38.7223),
                      'Bratislava': (17.1077, 48.1486)
                    },
    'line':   { 'color': 'darkblue',
                'width': 1.2,
                'style': '-',
                'alpha': 0.5
              },
    'marker': { 'color': 'orange',
                'size': marker_size,
                'style': '*',
                'alpha': 0.5
              },
}

eu_projects = [ai4eosc, imagine_ai]
n_projects = len(eu_projects)

# Get list of all cities and their coordinates
city_keys = []
cities = {}
for eup in eu_projects:
    city_keys += list(eup['destinations'].keys())
    cities = { **cities, **eup['destinations']}

# Find repeated cities, copy their coordinates
repeated_city_keys = list(duplicates(city_keys))
repeated_cities = {ckey: cvalue for ckey, cvalue in cities.items() if ckey in repeated_city_keys}
logger.debug(city_keys)
logger.debug(cities)
logger.debug(repeated_city_keys)
logger.debug(repeated_cities)

# Identify repeated city in the project, apply shift for better visualisation
for eup in eu_projects:
    for ckey, cvalue in eup['destinations'].items():
        if ckey in repeated_city_keys:
            lat = repeated_cities[ckey][1]
            eup['destinations'][ckey] = (cvalue[0], lat)
            repeated_cities[ckey] = (cvalue[0], lat + lat_shift)

# Shift Karlsruhe position for every project for better visibility
eup_i = 0
for eup in eu_projects:
    karlsruhe_coords_shift = (karlsruhe_coords[0],
                              karlsruhe_coords[1] + lat_shift*(eup_i - (n_projects - 1)/2))
    eup['destinations']['Karlsruhe'] = karlsruhe_coords_shift
    eup_i += 1
    logger.debug(eup)

# Create GeoDataFrame for cities
def city_geo(destinations):
    city_data = {
        'name': list(destinations.keys()),
        'lon': [lon for lon, lat in destinations.values()],
        'lat': [lat for lon, lat in destinations.values()],
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
        LineString([Point(destinations['Karlsruhe']), Point(coord)])
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


# Plotting
fig, ax = plt.subplots(figsize=(12, 12), dpi=200) # Bigger figure and higher DPI


# Clip the world data according to bbox for Europe
countries = countries.to_crs(epsg=4326)
countries = gpd.clip(countries, europe_bbox)
# Reproject only Europe as needed
countries = countries.to_crs(epsg=3857)
logger.info("Reprojected Europe")

# Select e.g. Spain from the countries GeoDataFrame
# Fill Spain with semi-transparent dark cyan
#spain = world[world['NAME'] == 'Spain'].to_crs(epsg=3857)
#spain.plot(ax=ax, color='darkcyan', alpha=0.5, edgecolor='darkcyan')

# Draw country boundaries
# vkoz@250418: borders are artificially cut by Europe bbox..
countries.boundary.plot(ax=ax, color='dimgray', linewidth=0.5, linestyle='--', antialiased=True, alpha=0.7)
logger.info("Added country borders")

for eup in eu_projects:
    draw_connections(eup)
    logger.info(f"Added project: {eup['name']}")

# Plot city names (we combine cities from all projects, because there can be duplicates otherwise)
cities = {  **imagine_ai['destinations'],
            **ai4eosc['destinations']
         }
logger.debug(cities)

# Show only Karlsruhe
#cities_gdf = city_geo({'Karlsruhe': karlsruhe_coords})
# Show all cities
cities_gdf = city_geo(cities)
cities_gdf = cities_gdf.to_crs(epsg=3857)
for x, y, label in zip(cities_gdf.geometry.x, cities_gdf.geometry.y, cities_gdf['name']):
    ax.text(x + 10000, y + 10000, label, fontsize=6)

logger.info("Added project cities")

#for x, y, label in zip(city_gdf.geometry.x, city_gdf.geometry.y, city_gdf['name']):
#    ax.text(x + 5000, y + 5000, label, fontsize=12, fontweight='bold', 
#            ha='center', va='center', color='black', 
#            bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle="round,pad=0.3"))

# Add OpenStreetMap basemap at a higher zoom level
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=basemap_zoom)
#ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=4)

plt.title("EU projects connections")
plt.axis('off')
plt.tight_layout()
plt.savefig("map_high_res.pdf", dpi=600, bbox_inches='tight')  # 300+ DPI = print quality
logger.info("Saved PDF")
plt.savefig("map_high_res.jpg", dpi=300, bbox_inches='tight')  # 300+ DPI = print quality
logger.info("Saved JPEG")
plt.show()
