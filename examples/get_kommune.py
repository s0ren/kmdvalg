"""# Get import"""
try:
    from kmdvalg import kommune
except ImportError:
    import sys, os
    sys.path.append( os.getcwd()+os.sep+"..")
    print("Path appended. This is dev code.")

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

"""# Get info all kommuner, synchronous mode"""
#df_sync = data.get_kommuner_df(make=True, async=False)
df_sync = data.get_kommuner_df(is_async=False)
#print(df_sync)

"""# Get info all kommuner, asyncio"""
df_async = data.get_kommuner_df(make=True, is_async=True)
#df_async = data.get_kommuner_df(async=True)
#print(df_async)

is_equal = df_sync.equals(df_async)
print("Are asyncio equal to sync?:", is_equal)

if not is_equal:
    print(df_sync)
    print(df_async)