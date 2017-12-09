# References

* [https://www.statsilk.com/maps/convert-esri-shapefile-map-geojson-format](https://www.statsilk.com/maps/convert-esri-shapefile-map-geojson-format)
* [https://help.github.com/articles/mapping-geojson-files-on-github/](https://help.github.com/articles/mapping-geojson-files-on-github/)
* [https://www.datavizforall.org/transform/mapshaper/](https://www.datavizforall.org/transform/mapshaper/)
* [https://github.com/mbloch/mapshaper/issues/194](https://github.com/mbloch/mapshaper/issues/194)
* [https://github.com/mbloch/mapshaper/wiki/Command-Reference](https://github.com/mbloch/mapshaper/wiki/Command-Reference)
* [http://spatialreference.org/ref/epsg/wgs-84-utm-zone-32n/](http://spatialreference.org/ref/epsg/wgs-84-utm-zone-32n/)


# Install mapshaper


```
# Node and mac
brew list | grep 'node'

# Possible install
brew install node
brew info node

# Find program
which node | xargs ls -l
which npm | xargs ls -l

# Install mapshaper
npm install -g mapshaper
```

# Convert to geojson

See current projection, in **ESRI WKT** format.

```
# Set variable
IN=Kommune_DAGI_1_2mio

# See proj
cat ${IN}.prj

PROJCS["ETRS_1989_UTM_Zone_32N",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",9.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]
```

With newlines

```
cat ${IN}.prj | tr ',' '\n'
```
Wee see the the zone:

```
PROJCS["ETRS_1989_UTM_Zone_32N
```

## Find input coordinate system
On [https://mygeodata.cloud/cs2cs/](https://mygeodata.cloud/cs2cs/), in '**Chose input coordinate system**' we search for **ETRS89 / UTM zone 32N**.

This gives **EPSG=25832** and Proj.4 text

```
+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs
```

## Find output coordinate system
On [https://mygeodata.cloud/cs2cs/](https://mygeodata.cloud/cs2cs/), in '**Chose output coordinate system**', the standard setting is **Pseudo-Mercator (EPSG:3857)**. See map here [https://epsg.io/3857](https://epsg.io/3857)

According to [wikimedia Mercator](https://en.wikipedia.org/wiki/Web_Mercator), then

> Web Mercator, Google Web Mercator, Spherical Mercator, WGS 84 Web Mercator or WGS 84/Pseudo-Mercator is a variant of the Mercator projection and is the de facto standard for Web mapping applications. It rose to prominence when Google Maps adopted it in 2005. It is used by virtually all major online map providers, including Google Maps, Bing Maps, OpenStreetMap, Mapquest, Esri, Mapbox, and many others.[3] Its official EPSG identifier is **EPSG:3857**, although others have been used historically.

This gives **EPSG=3857** and Proj.4 text

```
+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs
```

## Convert with mapshaper

Use 

* [EPSG:25832: https://epsg.io/25832 ](https://epsg.io/25832)
* [EPSG:3857: https://epsg.io/3857](https://epsg.io/3857)

```
# Set variable
IN=Kommune_DAGI_1_2mio

# Define coordinate system TO
TO="+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 
+y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs"

# Define coordinate system FROM
FROM="+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"

# Convert
mapshaper ${IN}.shp -simplify dp 20% -proj $TO from=$FROM -o format=geojson ${IN}.geojson
```