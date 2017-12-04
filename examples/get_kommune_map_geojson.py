"""# Get import"""
try:
    from kmdvalg import kommune
except ImportError:
    import sys, os
    sys.path.append( os.getcwd()+os.sep+"..")
    print(sys.path)

"""# Get import"""
from kmdvalg import kommune
import bokeh.plotting as bplt


"""# Get kommune map"""
kmap = kommune.kmap(make=True)

"""# Get plot import"""
from bqplot import pyplot as plt
from bqplot import *
import os

"""# Get plot"""
map_fig = plt.figure(title="Test")
map_res = plt.geo(map_data=topo_load(os.getcwd()+os.sep+"Kommune_DAGI_1_2mio.json"), stroke_color='black')

"""# Show output"""
# Get output. Either to Jupyter notebook or html file 
if True:
    if kommune.check_isnotebook():
        display(map_fig)