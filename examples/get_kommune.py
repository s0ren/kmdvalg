"""# Get import"""
try:
    from kmdvalg import kommune
except ImportError:
    import sys, os
    sys.path.append( os.getcwd()+os.sep+"..")
    print(sys.path)

"""# Get import"""
from kmdvalg import kommune

"""# Get kommune list"""
data = kommune.data()

# Extract from variable
data.get_kommuner()
kommuner = data.kommuner
for k in kommuner:
    print(k)

"""# Get info from københavn"""
dic_cph = data.get_kommune_dic('København')
for key in dic_cph:
    print(key, dic_cph[key])

"""# Get info all kommuner"""
df = data.get_kommuner_df(n=1)
print(df.head())