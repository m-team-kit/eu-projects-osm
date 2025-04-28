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
fig.patch.set_facecolor('white')    # Set white background

cfg.europe.plot(ax=ax, color='whitesmoke', edgecolor='dimgray', linewidth=0.5, linestyle='-', antialiased=True, alpha=0.7)
cfg.countries.plot(ax=ax, color='lightblue', edgecolor='dimgray', linewidth=0.5, linestyle='-', antialiased=True, alpha=0.7)
#cfg.countries.boundary.plot(ax=ax, color='dimgray', linewidth=0.5, linestyle='--', antialiased=True, alpha=0.7)

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
