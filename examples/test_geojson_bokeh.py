"""# Get import"""
try:
    from kmdvalg import kommune
except ImportError:
    import sys, os
    sys.path.append( os.getcwd()+os.sep+"..")
    print("Path appended. This is dev code.")

"""# Get import"""
from kmdvalg import kommune
import bokeh.plotting as bplt
import bokeh.models as bm
import json

"""# Denmark"""
data = os.getcwd()+os.sep+"Data"+os.sep+"DAGI_Kommunal_1_2mio_kortforsyningen"+os.sep+"Kommune_DAGI_1_2mio_EPSG.geojson"
with open(data, 'r') as f:
    # Read and replace
    t = f.read()
    t = t.replace("null", '{"type":"Point","coordinates":[]}')
    gs = bm.GeoJSONDataSource(geojson=t)

# Loop over json string
gsjon = json.loads(gs.geojson)
gs_feat = gsjon['features']
prop_keys = []
for feat in gs_feat:
    feat_geo = feat['geometry']
    feat_type = feat['type']
    feat_prop = feat['properties']
    for key in feat_prop:
        if key not in prop_keys:
            prop_keys.append(key)
            print(key, feat_prop[key])

wheel_zoom = bm.WheelZoomTool()
hover = bm.HoverTool(tooltips=[
    ("Navn", "@KOMNAVN"),
    ("KOMKODE", "@KOMKODE"),
    ("(Long, Lat)", "($x, $y)"),
    ("REGIONNAVN", "@REGIONNAVN"),
    #("REGIONKODE", "@REGIONKODE"),
    ("AREAL", "@AREAL"),
    ])
hover.point_policy = "follow_mouse"
tools = [bm.PanTool(), bm.BoxZoomTool(), wheel_zoom, bm.SaveTool(), bm.ResetTool(), bm.UndoTool(), bm.RedoTool(), bm.CrosshairTool(), hover]

fig = bplt.figure(title="Test", tools=tools, x_axis_location=None, y_axis_location=None, match_aspect=False)

# Activate scrool
fig.toolbar.active_scroll = wheel_zoom
# Remove grid lines
fig.grid.grid_line_color = None

#
from bokeh.palettes import RdYlGn11 as palette
palette.reverse()
#color_mapper = bm.LogColorMapper(palette=palette)
color_mapper = bm.LinearColorMapper(palette=palette)

#fig.patches(xs='xs', ys='ys', source=gs,
#    fill_alpha=0.7, line_color="white", line_width=0.5)
fig.patches(xs='xs', ys='ys', source=gs,
    fill_color={'field': 'AREAL', 'transform': color_mapper},
    fill_alpha=0.7, line_color="white", line_width=0.5)

"""# Show output"""
# Get output. Either to Jupyter notebook or html file 
if True:
    if kommune.check_isnotebook():
        from bokeh.io import output_notebook
        output_notebook()
        bplt.show(fig, notebook_handle=True)
    else:
        # Save to html
        filename = "bokeh.html"
        bplt.output_file(filename)
        bplt.save(fig)
        # And auto open
        import webbrowser, os
        webbrowser.open('file://' + os.path.realpath(filename))