"""# Get import"""
try:
    from kmdvalg import kommune
except ImportError:
    import sys, os
    sys.path.append( os.getcwd()+os.sep+"..")
    print("Path appended. This is dev code.")

"""# Get import"""
from kmdvalg import kommune
from bqplot import pyplot as plt
from bqplot import (
    Map, Mercator, Orthographic, ColorScale, ColorAxis,
    AlbersUSA, topo_load, Tooltip
)
import os

"""# Example 1"""
sc_geo = Mercator()
map_mark = Map(scales={'projection': sc_geo})
fig = plt.figure(marks=[map_mark], title='Basic Map Example')
if kommune.check_isnotebook():
    display(fig)

"""# Example 2"""
#sc_geo = Mercator()
sc_geo = Orthographic(scale_factor=375, center=[0, 25], rotate=(-50, 0))
map_mark = Map(map_data=topo_load('map_data/WorldMap.json'), scales={'projection': sc_geo}, 
        colors={682: 'Green', 356: 'Red', 643: '#0000ff', 'default_color': 'DarkOrange'})
fig = plt.figure(marks=[map_mark], fig_color='deepskyblue', title='Advanced Map Example')
if kommune.check_isnotebook():
    display(fig)
    
"""# Example 3"""
sc_geo = Mercator()
sc_c1 = ColorScale(scheme='YlOrRd')

map_styles = {'color': {643: 105., 4: 21., 398: 23., 156: 42., 124:78., 76: 98.},
              'scales': {'projection': sc_geo, 'color': sc_c1}, 'colors': {'default_color': 'Grey'}}

axis = ColorAxis(scale=sc_c1)

chloro_map = Map(map_data=topo_load('map_data/WorldMap.json'), **map_styles)
fig = plt.figure(marks=[chloro_map], axes=[axis],title='Choropleth Example')
if kommune.check_isnotebook():
    display(fig)
    
"""# Example 4"""
#sc_geo = Mercator(center=(-110,60), scale_factor=500)
sc_geo = AlbersUSA(translate=(500, 300), scale_factor=1200)

data = os.getcwd()+os.sep+"Data"+os.sep+"USCountiesMap.topojson"
map_mark = Map(map_data=topo_load(data), scales={'projection': sc_geo})
map_fig_1 = plt.figure(marks=[map_mark], fig_color='deepskyblue', title='Test for US map')

if kommune.check_isnotebook():
    display(map_fig_1)
    
"""# Denmark"""
sc_geo = Mercator(center=(11,56.7), scale_factor=7000)

data = os.getcwd()+os.sep+"Data"+os.sep+"DAGI_Kommunal_1_2mio_kortforsyningen"+os.sep+"Kommune_DAGI_1_2mio_EPSG.geojson"
map_mark_dk = Map(map_data=topo_load(data), scales={'projection': sc_geo})

map_style_eu = {'scales': {'projection': sc_geo}, 'colors': {'default_color': 'Grey'}}
map_mark_eu = Map(map_data=topo_load('map_data/EuropeMap.json'), **map_style_eu)

map_fig_1 = plt.figure(marks=[map_mark_eu, map_mark_dk], fig_color='deepskyblue', title='Test for Denmark Kommune map')

if kommune.check_isnotebook():
    display(map_fig_1)