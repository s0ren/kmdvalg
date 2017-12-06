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

"""# Get kommune list"""
data = kommune.data()
# Get info, by async to speed up by factor 10x.
df = data.get_kommuner_df(make=True, async=True)

"""# Get kommune map from shapefiles"""
#kmap = kommune.kmap(make=True)
kmap = kommune.kmap()

# Combine map data with voting data.
kmap.make_map_source(df=df)

fig = kmap.get_map()

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