import geopandas as gpd
from shapely.geometry import box

# how detailed map to save, larger number - more details
basemap_zoom = 7

# Default values for drawing projects (can be individually rewritten)
# line width
line_width = 2
line_style = '-'
line_alpha = 0.5
# size of the city marker
marker_size = 10
marker_style = 'o'
marker_alpha = 0.8
# legend: marker size
legend_marker_size = 6
legend_loc='lower center' #'lower left'
legend_bbox_to_anchor=(0.5, -0.1)
legend_fontsize = 9

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

# Function to init a project
def init_project(name):
    project = {
        'name': name,
        'destinations': { 'Karlsruhe' : karlsruhe_coords },
        'line':   { 'color': 'gray',
                    'width': line_width,
                    'style': line_style,
                    'alpha': line_alpha
                  },
        'marker': { 'color': 'darkgray',
                    'size' : marker_size,
                    'style': marker_style,
                    'alpha': marker_alpha
                  },
    }
    return project
        

# Define AI4EOSC destination cities
ai4eosc = init_project('AI4EOSC')
ai4eosc['destinations'].update({ 
    'Valencia': (-0.3763, 39.4699),
    'Santander': (-3.8044, 43.4623),
    'Lisboa': (-9.1393, 38.7223),
    'Bologne': (11.3426, 44.4949),
    'Poznan': (16.9252, 52.4064),
    'Bratislava': (17.1077, 48.1486)
})
ai4eosc['line']['color']   = 'darkcyan'
ai4eosc['marker']['color'] = 'deeppink'

# Define iMagine-AI destination cities
imagine_ai = init_project('iMagine')
imagine_ai['destinations'].update({
    'Valencia': (-0.3763, 39.4699),
    'Santander': (-3.8044, 43.4623),
    'Lisboa': (-9.1393, 38.7223),
    'Bratislava': (17.1077, 48.1486)
})
imagine_ai['line']['color'] = 'darkblue'
imagine_ai['marker']['color'] = 'orange'

aasas = init_project('AASAS')

eosc_beyond = init_project('EOSC Beyond')

aarctree = init_project('AARC Tree')

intertwin = init_project('interTWIN')

skills4eosc = init_project('Skills4EOSC')

aquainfra = init_project('AquaINFRA')

nffa_europe = init_project('NFFA Europe PILOT - NEP')

eu_projects = [ai4eosc, imagine_ai,
               aasas, eosc_beyond,
               aarctree, intertwin,
               skills4eosc, aquainfra,
               nffa_europe]

# Define a bounding box for Europe in EPSG:4326 (lon/lat)
#  "minx": -25,   # westernmost (e.g., Portugal/Iceland)
#  "maxx": 45,    # easternmost (e.g., Slovakia/Ukraine)
#  "miny": 34,    # southernmost (e.g., Mediterranean)
#  "maxy": 72     # northernmost (e.g., Scandinavia)
#  box(minx, miny, maxx, maxy)
europe_bbox = box(-25, 32, 40, 60)

