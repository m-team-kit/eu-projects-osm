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

europe_countries = ['Albania', 'Andora', 'Austria', 'Belgium', 'Bulgraia', 'Croatia', 'Cyprus', 'Czechia',
                    'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece',
                    'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg',
                    'Malta', 'Monaco', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'San Marino', 
                    'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'United Kingdom']

europe = world[world['NAME'].isin(europe_countries)]

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
    'Lisbon': (-9.1393, 38.7223),
    'Bologne': (11.3426, 44.4949),
    'Poznan': (16.9252, 52.4064),
    'Bratislava': (17.1077, 48.1486)
})
ai4eosc['line']['color']   = 'darkcyan'
ai4eosc['marker']['color'] = 'deeppink'

# Define iMagine-AI destination cities
imagine_ai = init_project('iMagine')
imagine_ai['destinations'].update({
    'Amsterdam': (4.9041, 52.3676),
    'Ankara': (32.8541, 39.9208),
    'Lecce': (18.1743, 40.3529),
    'Santander': (-3.8044, 43.4623),
    'Oldenburg': (8.2146, 53.1435),
    #'Bremen': (8.8017, 53.0793),
    'Brest': (-4.4861, 48.3904),
    'Galway': (-9.0568, 53.2707),
    'Barcelona': (2.1734, 41.3851),
    'Bratislava': (17.1077, 48.1486),
    'Lisbon': (-9.1399, 38.7169),
    'Nootdorp': (4.4111, 52.0447),
    'Trieste': (13.7768, 45.6495),
    'Valencia': (-0.3763, 39.4699),
    'Palma de Mallorca': (2.6502, 39.5696),
    'Paris': (2.3522, 48.8566),
    'Metz': (6.1757, 49.1193),
    'Oostende': (2.9200, 51.2300),
    'Waterford': (-7.1101, 52.2593),
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

