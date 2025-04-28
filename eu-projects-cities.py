import config as cfg
import geopandas as gpd
import logging
import matplotlib.pyplot as plt
import contextily as ctx
from config import eu_projects, karlsruhe_coords, lat_shift
from iteration_utilities import duplicates, unique_everseen
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from shapely.geometry import Point, LineString

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # 0: Not set, 10: DEBUG, 20: INFO, 30: WARNING, 40: ERROR, 50: CRITICAL

# create console handler and set level to debug
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#logger.addHandler(ch)

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

n_projects = len(eu_projects)

# Get list of all cities and their coordinates
city_keys = []
cities = {}
for eup in eu_projects:
    city_keys += list(eup['destinations'].keys())
    cities = { **cities, **eup['destinations']}

# Find repeated cities, copy their coordinates
repeated_city_keys = list(unique_everseen(duplicates(city_keys)))
# Remove Karlsruhe from repeated cities
repeated_city_keys.remove('Karlsruhe') if 'Karlsruhe' in repeated_city_keys else None
# Create dictionary with coordinates of repeated cities
repeated_cities = {ckey: cvalue for ckey, cvalue in cities.items() if ckey in repeated_city_keys}
logger.debug(f"cities in projects: {city_keys}")
logger.debug(f"city coordinates: {cities}")
logger.debug(f"repeated_city_keys: {repeated_city_keys}")
logger.debug(f"repeated_cities: {repeated_cities}")

# Identify repeated city in the project, apply shift for better visualisation
for eup in eu_projects:
    for ckey, cvalue in eup['destinations'].items():
        if ckey in repeated_city_keys:
            lat = repeated_cities[ckey][1]
            eup['destinations'][ckey] = (cvalue[0], lat)
            repeated_cities[ckey] = (cvalue[0], lat + lat_shift)

# Option: Shift Karlsruhe position for every project for better visibility
eup_i = 0
#for eup in eu_projects:
#    karlsruhe_coords_shift = (karlsruhe_coords[0],
#                              karlsruhe_coords[1] + lat_shift*(eup_i - (n_projects - 1)/2))
#    eup['destinations']['Karlsruhe'] = karlsruhe_coords_shift
#    eup_i += 1
#    logger.debug(eup)

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

# Function to draw lines between Karlsruhe and project city
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


# Create legend for the plot
legend_elements = []
for eup in eu_projects:
    legend_elements.append(
        plt.Line2D([0], [0], marker=eup['marker']['style'],
                   markerfacecolor=eup['marker']['color'],
                   markersize=cfg.legend_marker_size,
                   markeredgewidth=0, color=eup['line']['color'],
                   alpha=eup['line']['alpha'], label=eup['name']),
    )

# Plotting
fig, ax = plt.subplots(figsize=(12, 12), dpi=200) # Bigger figure and higher DPI

# Clip the world data according to bbox for Europe
countries = cfg.countries.to_crs(epsg=4326)
countries = gpd.clip(countries, cfg.europe_bbox)
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
# Show Karlsruhe
cities_gdf = city_geo({'Karlsruhe': karlsruhe_coords})
# Show all cities
logger.debug(cities)
cities_gdf = city_geo(cities)
cities_gdf = cities_gdf.to_crs(epsg=3857)
for x, y, label in zip(cities_gdf.geometry.x, cities_gdf.geometry.y, cities_gdf['name']):
    ax.text(x + 10000, y + 10000, label, fontsize=6)

logger.info("Added project cities")

# Add OpenStreetMap basemap at a higher zoom level 
# options: OpenStreetMap.Mapnik (default), CartoDB.Positron
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=cfg.basemap_zoom)

plt.title("EU projects connections")
plt.axis('off')
plt.tight_layout()
ax.legend(handles=legend_elements, 
    ncol=2,
    numpoints=2,
    loc=cfg.legend_loc,
    bbox_to_anchor=cfg.legend_bbox_to_anchor,
    fontsize=cfg.legend_fontsize
)
plt.savefig("map_high_res.pdf", dpi=600, bbox_inches='tight')  # 300+ DPI = print quality
logger.info("Saved PDF")
plt.savefig("map_high_res.jpg", dpi=300, bbox_inches='tight')  # 300+ DPI = print quality
logger.info("Saved JPEG")
plt.show()
