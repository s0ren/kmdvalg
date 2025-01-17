# -*- coding: utf-8 -*-
import os.path, os

def check_isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            # Jupyter notebook or qtconsole
            return True
        elif shell == 'TerminalInteractiveShell':
            # Terminal running IPython
            return False
        else:
            # Other type (?)
            return False
    except NameError:
         # Probably standard Python interpreter
        return False

class data:
    def __init__(self,):
        pass

    def get_kommuner(self):
        from bs4 import BeautifulSoup
        import requests

        # Get the page
        r = requests.get('https://www.kmdvalg.dk/Main/Home/KV')
        # Make soup
        soup = BeautifulSoup(r.text, "html.parser")

        # Get kommune items
        kmd_list_items = soup.find("div", {"class": "col-sm-12 content-block kmd-list-items"})
        
        # Find lists in kommune
        kmd_list_items_group = kmd_list_items.find_all("div", {"class": "list-group"})

        # Loop over letter in groups
        kommuner = []
        kommuner_links = {}
        for group in kmd_list_items_group:
            list_group_item = group.find("div", {"class": "list-group-item"})
            group_links = group.find_all('a')
            for link in group_links:
                #print(list_group_item.text, link.text)
                kommuner.append([list_group_item.text.strip(), link.text.strip(), link['href']])
                kommuner_links[link.text.strip()] = link['href']

        self.kommuner = kommuner
        self.kommuner_links = kommuner_links

    def get_kommune_dic_list(self):
        import asyncio
        # Check if exists
        if not hasattr(self, 'kommuner_links'):
            self.get_kommuner()

        # Unpack
        _, kommuner, kommune_links = zip(*self.kommuner)

        loop = asyncio.get_event_loop()
        d_list = loop.run_until_complete(self.get_kommune_dic_async(kommuner=kommuner, kommune_links=kommune_links))
        return d_list

    async def get_kommune_dic_async(self, kommuner=None, kommune_links=None):
        import asyncio
        import concurrent.futures
        import requests
        nw = len(kommune_links)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            loop = asyncio.get_event_loop()
            futures = []
            # Make list of threads to be called
            for i in range(nw):
                futures.append(loop.run_in_executor(executor, requests.get, kommune_links[i]))
            # Process them
            i = 0
            d_list = []
            for response in await asyncio.gather(*futures):
                kommune = kommuner[i]
                d = self.get_dic_from_request(r=response, kommune=kommune)
                d_list.append(d)
                i += 1
        return d_list

    
    def get_kommune_dic(self, kommune=None):
        import requests
        # Check if exists
        if not hasattr(self, 'kommuner_links'):
            self.get_kommuner()

        # Get link
        link = self.kommuner_links[kommune]
        # Get the page
        r = requests.get(link)
        r.encoding = 'utf-8'
        d = self.get_dic_from_request(r=r, kommune=kommune)
        return d


    def get_party_votes_from_request(self, kommune, r):
        from bs4 import BeautifulSoup

        parti_votes = {}

        # Make soup
        #soup = BeautifulSoup(r.text, "html.parser", from_encoding="utf-8")
        #soup = BeautifulSoup(r.text, features="html.parser", from_encoding="utf-8")
        soup = BeautifulSoup(r.text, features="html.parser")

        # Get box data
        kmd_parti_list = soup.find("div", {"class": "kmd-parti-list"})

        # get columns
        for parti in kmd_parti_list.findAll("div", {"class": "row table-like-row"})[1:]:
            columns = parti.findAll("div", {"class", "table-like-cell"})
            # print(columns[0].text)
            # print(columns[0])
            print(columns[0])
            #print(columns[0].decode('utf-8').text)
            
            parti_dict = {
                "Kandidatliste"   : (columns[0].span.text, columns[0].a.text),
                "Stemmetal"       : int(columns[1].text.replace(".", "")),
                "Tilvækst"        : int(columns[2].text.replace(".", "")),
                #"Procent"         : float(columns[3].text.replace(",", ".")),
                #"ProcentTilvækst" : float(columns[4].text.replace(",", ".")),
            }
            parti_votes[parti_dict["Kandidatliste"][1]] = parti_dict
        #print(parti_votes)
        return parti_votes

    
    def get_polling_stations_from_request(self, kommune, r):
        from bs4 import BeautifulSoup

        stattions = {}

        # Make soup
        #soup = BeautifulSoup(r.text, "html.parser", from_encoding="utf-8")
        #soup = BeautifulSoup(r.text, features="html.parser", from_encoding="utf-8")
        soup = BeautifulSoup(r.text, features="html.parser")

        # Get box data
        kmd_vote_areas = soup.find("div", {"id": "vote-areas"})

        # get columns
        for area in kmd_vote_areas.findAll("div", {"class": "row table-like-row"})[1:]:
            columns = area.findAll("div", {"class", "table-like-cell"})
            # print(columns[0].text)
            # print(columns[0])
            print(columns[0])
            #print(columns[0].decode('utf-8').text)
            
            parti_dict = {
                "Kandidatliste"   : (columns[0].span.text, columns[0].a.text),
                "Stemmetal"       : int(columns[1].text.replace(".", "")),
                "Tilvækst"        : int(columns[2].text.replace(".", "")),
                #"Procent"         : float(columns[3].text.replace(",", ".")),
                #"ProcentTilvækst" : float(columns[4].text.replace(",", ".")),
            }
            parti_votes[parti_dict["Kandidatliste"][1]] = parti_dict
        #print(parti_votes)
        return parti_votes
   
    def get_dic_from_request(self, r, kommune):
        from bs4 import BeautifulSoup
        # Make soup
        soup = BeautifulSoup(r.text, "html.parser")

        # Get columns with data
        col_xs_6_list = soup.find_all("td", {"class": "col-xs-6"})
        for i, col_xs_6 in enumerate(col_xs_6_list):
            if "Antal stemmeberettigede" in col_xs_6.text:
                Antal_stemmeberettigede = [col_xs_6.text, int(col_xs_6.findNext('td').text.replace(".", ""))]
            if "Afstemningsomr" in col_xs_6.text:
                Afstemningsomr = [col_xs_6.text, int(col_xs_6.findNext('td').text)]
            if "I alt gyldige stemmer" in col_xs_6.text:
                I_alt_gyldige_stemmer = [col_xs_6.text, int(col_xs_6.findNext('td').text.replace(".", ""))]
            if "I alt afgivne stemmer" in col_xs_6.text:
                I_alt_afgivne_stemmer = [col_xs_6.text, int(col_xs_6.findNext('td').text.replace(".", ""))]

        # Calculate vote percentage
        stemme_pct = ["Stemme pct.", round(I_alt_afgivne_stemmer[-1] / Antal_stemmeberettigede[-1] *100, 2)]
        # Make dictionary with data
        d = {
            'kommune' : ["Kommune", kommune],
            'Antal_stemmeberettigede' : Antal_stemmeberettigede,
            'Afstemningsomr' : Afstemningsomr,
            'I_alt_gyldige_stemmer' : I_alt_gyldige_stemmer,
            'I_alt_afgivne_stemmer' : I_alt_afgivne_stemmer,
            'stemme_pct' : stemme_pct,
            'party_votes' : self.get_party_votes_from_request(kommune, r),
            'polling_stations' : self.get_polling_stations_from_request(kommune, r)
        }

        #polling_stations = get_polling_stations_from_request(kommune, r)

        return d
 
    def get_kommuner_df(self, n=None, make=False, is_async=False):
        import pandas as pd
        import pickle

        # If file exists
        if not is_async:
            df_file = "Valg2017_kommune.pkl"
        else:
            df_file = "Valg2017_kommune_async.pkl"

        if os.path.isfile(df_file) and not make:
            print("Kommune data exists. Reading it.")
            df = pd.read_pickle(df_file)
        else:
            print("Kommune data missing. Creating it.")
            if not hasattr(self, 'kommuner'):
                self.get_kommuner()

            # Loop over kommuner
            if not is_async:
                if n:
                    kommuner = self.kommuner[:n]
                else:
                    kommuner = self.kommuner

                kommune_dic_list = []
                for kommune in kommuner:
                    print("Reading for:", kommune)
                    # Get kommune
                    kommune_dic = self.get_kommune_dic(kommune[1])
                    kommune_dic_list.append(kommune_dic)
            else:
                # asyncio
                kommune_dic_list = self.get_kommune_dic_list()

            # Collect
            kommune_list = []
            Antal_stemmeberettigede_list = []
            Afstemningsomr_list = []
            I_alt_gyldige_stemmer_list = []
            I_alt_afgivne_stemmer_list = []
            stemme_pct_list = []
            for kommune_dic in kommune_dic_list:
                # Append to lists
                kommune_list.append(kommune_dic['kommune'][-1])
                Antal_stemmeberettigede_list.append(kommune_dic['Antal_stemmeberettigede'][-1])
                Afstemningsomr_list.append(kommune_dic['Afstemningsomr'][-1])
                I_alt_gyldige_stemmer_list.append(kommune_dic['I_alt_gyldige_stemmer'][-1])
                I_alt_afgivne_stemmer_list.append(kommune_dic['I_alt_afgivne_stemmer'][-1])
                stemme_pct_list.append(kommune_dic['stemme_pct'][-1])
            
            # Make dictionary to pandas
            d = {
                'Kommune' : kommune_list,
                'Stemmeberettigede' : Antal_stemmeberettigede_list,
                'Afstemningsomr' :Afstemningsomr_list,
                'Gyldige_stemmer' : I_alt_gyldige_stemmer_list,
                'Afgivne_stemmer' : I_alt_afgivne_stemmer_list,
                'stemme_pct' : stemme_pct_list
            }
            # Create
            df = pd.DataFrame.from_dict(d)
            # Re-order
            df = df[['Kommune', 'Stemmeberettigede', 'Afstemningsomr', 'Gyldige_stemmer', 'Afgivne_stemmer', 'stemme_pct']]
            # Store
            df.to_pickle(df_file)

        return df
    
class kmap:
    # Data fra https://download.kortforsyningen.dk
    # "Indeholder data fra Styrelsen for Dataforsyning og Effektivisering”
    # Navnet på datasættet(ene): Digdag (Kommunal)
    # Tidspunkt, hvor datasættet(ene) er hentet hos myndigheden, eller om der er tale om en datatjeneste. : 2017/12/03
    def __init__(self, make=False):
        import pickle

        # If file exists
        self.dic_file = "Kommune.pkl"
        if os.path.isfile(self.dic_file) and not make:
            print("Kommune shapefile exists. Reading it.")
            with open(self.dic_file, 'rb') as f:
                self.kdic = pickle.load(f)
        # Create it
        else:
            # Create from history dataset
            #self.make_map_Digdag_Kommunal()

            # Create from thinnned dataset
            self.make_map_DAGI_Kommunal()

    def make_map_DAGI_Kommunal(self):
        print("Kommune shapefile missing. Creating it.")
        import shapefile
        import datetime
        import numpy as np
        import pickle

        myshp = open("Data"+os.sep+"DAGI_Kommunal_1_2mio_kortforsyningen"+os.sep+"Kommune_DAGI_1_2mio.shp", "rb")
        mydbf = open("Data"+os.sep+"DAGI_Kommunal_1_2mio_kortforsyningen"+os.sep+"Kommune_DAGI_1_2mio.dbf", "rb")
        sf = shapefile.Reader(shp=myshp, dbf=mydbf)
        sf_list = list(sf.shapeRecords())
        print('number of shapes imported:',len(sf.shapes()) )

        # Collect
        kommuner_list = []
        kommune_dates_list = []
        x_lon_list = []
        y_lat_list = []
        stemme_pct_list = []
        self.kdic = {}
        j = 0
        for i, shape in enumerate(sf_list):
            # Get datetime
            kommune_date = shape.record[9] # [-1]
            # Get kommune
            kdata = shape.record[12]
            if isinstance(kdata, (bytes, bytearray)):
                kommune = kdata.decode("latin-1")
            else:
                kommune = kdata

            npoints=len(shape.shape.points) # total points
            nparts = len(shape.shape.parts) # total parts
            if nparts == 1:
                x_lon = np.zeros((len(shape.shape.points),1))
                y_lat = np.zeros((len(shape.shape.points),1))
                for ip in range(len(shape.shape.points)):
                    x_lon[ip] = shape.shape.points[ip][0]
                    y_lat[ip] = shape.shape.points[ip][1]
                # Collect
                kommuner_list.append(kommune)
                kommune_dates_list.append(kommune_date.strftime("%Y-%m-%d"))
                x_lon_list.append(x_lon)
                y_lat_list.append(y_lat)
                # Add to counter
                j += 1

            else: # loop over parts of each shape, plot separately
                for ip in range(nparts): # loop over parts, plot separately
                    i0=shape.shape.parts[ip]
                    if ip < nparts-1:
                        i1 = shape.shape.parts[ip+1]-1
                    else:
                        i1 = npoints

                    seg=shape.shape.points[i0:i1+1]
                    x_lon = np.zeros((len(seg),1))
                    y_lat = np.zeros((len(seg),1))
                    for ip in range(len(seg)):
                        x_lon[ip] = seg[ip][0]
                        y_lat[ip] = seg[ip][1]
                    # Collect
                    kommuner_list.append(kommune)
                    kommune_dates_list.append(kommune_date.strftime("%Y-%m-%d"))
                    x_lon_list.append(x_lon)
                    y_lat_list.append(y_lat)
                # Add to counter
                j += 1

        # Print
        print('number of shapes stored:', j )
        # Store all kommuner
        self.kdic['kommuner'] = kommuner_list
        self.kdic['x_lon'] = x_lon_list
        self.kdic['y_lat'] = y_lat_list
        self.kdic['kommuner_dates'] = kommune_dates_list
        # Save
        with open(self.dic_file, 'wb') as f:
            pickle.dump(self.kdic, f, pickle.HIGHEST_PROTOCOL)

    def make_map_Digdag_Kommunal(self):
        print("Kommune shapefile missing. Creating it.")
        import shapefile
        import datetime
        import numpy as np
        import pickle

        myshp = open("Data"+os.sep+"Digdag_Kommunal_kortforsyningen"+os.sep+"Kommune_Digdag_Kommunal.shp", "rb")
        mydbf = open("Data"+os.sep+"Digdag_Kommunal_kortforsyningen"+os.sep+"Kommune_Digdag_Kommunal.dbf", "rb")
        sf = shapefile.Reader(shp=myshp, dbf=mydbf)
        sf_list = list(sf.shapeRecords())
        print('number of shapes imported:',len(sf.shapes()) )

        kommune_date_min = datetime.datetime.strptime('2006-01-01', '%Y-%m-%d')
        # From: https://chrishavlin.wordpress.com/2016/11/16/shapefiles-tutorial/
        # First loop to check time
        sel_kommuner = []
        sel_times = []
        for i, shape in enumerate(sf_list):
            # Get date string and store
            kommune_date_str = shape.record[3]
            # Get time object
            kommune_date = datetime.datetime.strptime(kommune_date_str, '%Y-%m-%d')
            # Skip if shape time is less than minimum date
            if kommune_date < kommune_date_min:
                continue
            # Get kommune
            kdata = shape.record[1]
            if isinstance(kdata, (bytes, bytearray)):
                kommune = kdata.decode("latin-1")
            else:
                kommune = kdata
            kommune = kommune.split(" Kommune")[0]
            # Test kommune exists
            if kommune not in sel_kommuner:
                sel_kommuner.append(kommune)
                sel_times.append(kommune_date)
            else:
                index = sel_kommuner.index(kommune)
                prev_time = sel_times[index]
                # Replace
                if kommune_date > prev_time:
                    sel_times[index] = kommune_date

        # Loop again
        # Collect
        kommuner_list = []
        kommune_dates_list = []
        x_lon_list = []
        y_lat_list = []
        stemme_pct_list = []
        self.kdic = {}

        j = 0
        for i, shape in enumerate(sf_list):
            # Get kommune
            kdata = shape.record[1]
            if isinstance(kdata, (bytes, bytearray)):
                kommune = kdata.decode("latin-1")
            else:
                kommune = kdata
            kommune = kommune.split(" Kommune")[0]
            # Get date string and store
            kommune_date_str = shape.record[3]
            # Get time object
            kommune_date = datetime.datetime.strptime(kommune_date_str, '%Y-%m-%d')
            if kommune in sel_kommuner:
                index = sel_kommuner.index(kommune)
                prev_time = sel_times[index]
                # If time matches from before
                if kommune_date == prev_time:
                    npoints=len(shape.shape.points) # total points
                    nparts = len(shape.shape.parts) # total parts
                    if nparts == 1:
                        x_lon = np.zeros((len(shape.shape.points),1))
                        y_lat = np.zeros((len(shape.shape.points),1))
                        for ip in range(len(shape.shape.points)):
                            x_lon[ip] = shape.shape.points[ip][0]
                            y_lat[ip] = shape.shape.points[ip][1]
                        # Collect
                        kommuner_list.append(kommune)
                        kommune_dates_list.append(kommune_date_str)
                        x_lon_list.append(x_lon)
                        y_lat_list.append(y_lat)
                        # Add to counter
                        j += 1

                    else: # loop over parts of each shape, plot separately
                        for ip in range(nparts): # loop over parts, plot separately
                            i0=shape.shape.parts[ip]
                            if ip < nparts-1:
                                i1 = shape.shape.parts[ip+1]-1
                            else:
                                i1 = npoints

                            seg=shape.shape.points[i0:i1+1]
                            x_lon = np.zeros((len(seg),1))
                            y_lat = np.zeros((len(seg),1))
                            for ip in range(len(seg)):
                                x_lon[ip] = seg[ip][0]
                                y_lat[ip] = seg[ip][1]
                            # Collect
                            kommuner_list.append(kommune)
                            kommune_dates_list.append(kommune_date_str)
                            x_lon_list.append(x_lon)
                            y_lat_list.append(y_lat)
                        # Add to counter
                        j += 1
        # Print
        print('number of shapes stored:', j )
        # Store all kommuner
        self.kdic['kommuner'] = kommuner_list
        self.kdic['x_lon'] = x_lon_list
        self.kdic['y_lat'] = y_lat_list
        self.kdic['kommuner_dates'] = kommune_dates_list
        # Save
        with open(self.dic_file, 'wb') as f:
            pickle.dump(self.kdic, f, pickle.HIGHEST_PROTOCOL)

    def make_map_source(self, df=None):
        import bokeh.models as bm

        # Test if there exists data
        if type(df) != type(None):
            # Make copy of dict
            kdic = self.kdic.copy()
            # Collect
            stemme_pct_list = []
            # Loop through dic
            for i, kommune in enumerate(kdic['kommuner']):
                #kommune_date = kdic['kommuner_dates'][i]
                #print(kommune.replace("Aa", "Å"))
                if kommune in df['Kommune'].values:
                    stemme_pct = df.loc[df['Kommune'] == kommune, 'stemme_pct'].iloc[0]
                    stemme_pct_list.append(stemme_pct)
                # If s is added
                elif kommune[:-1] in df['Kommune'].values:
                    stemme_pct = df.loc[df['Kommune'] == kommune[:-1], 'stemme_pct'].iloc[0]
                    stemme_pct_list.append(stemme_pct)
                elif kommune+"s" in df['Kommune'].values:
                    stemme_pct = df.loc[df['Kommune'] == kommune+"s", 'stemme_pct'].iloc[0]
                    stemme_pct_list.append(stemme_pct)
                elif kommune.replace("Å", "Aa").replace("å", "aa").replace("Høje Taastrup","Høje-Taastrup") in df['Kommune'].values:
                    stemme_pct = df.loc[df['Kommune'] == kommune.replace("Å", "Aa").replace("å", "aa").replace("Høje Taastrup","Høje-Taastrup"), 'stemme_pct'].iloc[0]
                    stemme_pct_list.append(stemme_pct)
                else:
                    #print(kommune, "Not found")
                    stemme_pct_list.append(None)
            # append
            kdic['stemme_pct'] = stemme_pct_list
            # Create data
            self.source = bm.ColumnDataSource(data=kdic)
            
        else:
            print("Making source from map")
            self.source = bm.ColumnDataSource(data=self.kdic)

    def get_map(self):
        import bokeh.plotting as bplt
        import bokeh.models as bm

        wheel_zoom = bm.WheelZoomTool()
        self.hover = bm.HoverTool(tooltips=[
            ("Navn", "@kommuner"),
            #("(Long, Lat)", "($x, $y)"),
            ("Dato", "@kommuner_dates"),
            ("stemme pct", "@stemme_pct %"),
            ])
        self.hover.point_policy = "follow_mouse"
        tools = [bm.PanTool(), bm.BoxZoomTool(), wheel_zoom, bm.SaveTool(), bm.ResetTool(), bm.UndoTool(), bm.RedoTool(), bm.CrosshairTool(), self.hover]
        fig = bplt.figure(title="Test", tools=tools, x_axis_location=None, y_axis_location=None, match_aspect=True)
        # Activate scrool
        fig.toolbar.active_scroll = wheel_zoom
        # Remove grid lines
        fig.grid.grid_line_color = None

        # Check if source exists
        if not hasattr(self, 'source'):
            self.make_map_source()

        # Make color mapper
        #from bokeh.palettes import Viridis6 as palette
        #from bokeh.palettes import Spectral11 as palette
        from bokeh.palettes import RdYlGn11 as palette
        palette.reverse()
        #color_mapper = bm.LogColorMapper(palette=palette, high=90., low=50.)
        color_mapper = bm.LinearColorMapper(palette=palette, high=90., low=50.)

        # Plot
        fig.patches(xs='x_lon', ys='y_lat', source=self.source,
            fill_color={'field': 'stemme_pct', 'transform': color_mapper},
            fill_alpha=0.7, line_color="white", line_width=0.5)

        return fig