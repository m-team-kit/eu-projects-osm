import geopandas as gpd
from shapely.geometry import box

# how detailed map to save, larger number - more details
basemap_zoom = 5
# line width
line_width = 2
# size of the city marker
marker_size = 10
marker_style = 'o'
legend_marker_size = 5

# how much shift lat for repeated cities
lat_shift = 0.15

# Load world map data
world = gpd.read_file("data/ne_50m_admin_0_countries.shp")

# Filter for countries you want to show (e.g., in Europe)
countries = world[world['NAME'].isin(['Spain', 'Germany', 'France', 
                                      'Italy', 'Belgium', 'Netherlands', 
                                      'Poland', 'Portugal', 'Slovakia',
                                      'Ireland', 'Turkey', 'Denmark',
                                      'Norway', 'Sweden', 'United Kingdom'])]

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
                'width': line_width,
                'style': '-',
                'alpha': 0.5
              },
    'marker': { 'color': 'deeppink',
                'size' : marker_size,
                'style': marker_style,
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
                'width': line_width,
                'style': '-',
                'alpha': 0.5
              },
    'marker': { 'color': 'orange',
                'size' : marker_size,
                'style': marker_style,
                'alpha': 0.5
              },
}

eu_projects = [ai4eosc, imagine_ai]

# Define a bounding box for Europe in EPSG:4326 (lon/lat)
#  "minx": -25,   # westernmost (e.g., Portugal/Iceland)
#  "maxx": 45,    # easternmost (e.g., Slovakia/Ukraine)
#  "miny": 34,    # southernmost (e.g., Mediterranean)
#  "maxy": 72     # northernmost (e.g., Scandinavia)
#  box(minx, miny, maxx, maxy)
europe_bbox = box(-25, 32, 40, 60)

