"""# Get import"""
try:
    from kmdvalg import kommune
except ImportError:
    import sys, os
    sys.path.append( os.getcwd()+os.sep+"..")
    print(sys.path)

"""# Get import"""
from kmdvalg import kommune

"""# Get plot import"""
from bqplot import pyplot as plt
from bqplot import *
import os

"""# Get example plot"""
map_fig_1 = plt.figure(title="Test for US map 1")
_ = plt.geo(map_data=topo_load(os.getcwd()+os.sep+"Data"+os.sep+"USCountiesMap.topojson"), stroke_color='black')

map_fig_2 = plt.figure(title="Test for US map 2")
_ = plt.geo(map_data=topo_load(os.getcwd()+os.sep+"Data"+os.sep+"USCountiesMap.topojson"), stroke_color='green')


"""# Get own plot"""
# Map is converted online here: http://mapshaper.org/
# First unzip, "KOMMUNAL_SHAPE_UTM32-EUREF89.zip" 
# Then zip only "Kommune.*" files to a single zip.
# Upload Kommune.zip

# https://help.github.com/articles/mapping-geojson-files-on-github/
# https://www.datavizforall.org/transform/mapshaper/
# https://github.com/mbloch/mapshaper/issues/194
# https://github.com/mbloch/mapshaper/wiki/Command-Reference
# http://spatialreference.org/ref/epsg/wgs-84-utm-zone-32n/
# In console
# -projections
# -proj +proj=utm +zone=32N, +ellps=WGS84 +datum=WGS84 +units=m
# -proj wgs84
# -proj +proj=longlat +datum=WGS84 +no_defs from='+proj=tmerc +lat_0=0 +lon_0=114 +k=1.000000 +x_0=500000 +y_0=0 +ellps=krass +units=m +no_defs'
# -proj +proj=longlat +datum=WGS84 +no_defs from='+proj=utm +zone=32N, +ellps=WGS84 +datum=WGS84 +units=m'


# Click "simplyfy", keep standard settings, lower to 0.0%.
# Export to TopoJson


#map_res = plt.geo(map_data=topo_load(os.getcwd()+os.sep+"Kommune_DAGI_1_2mio.json"), stroke_color='black')

"""# Show output"""
# Get output. Either to Jupyter notebook or html file 
if True:
    if kommune.check_isnotebook():
        display(map_fig_1)
        display(map_fig_2)        
        