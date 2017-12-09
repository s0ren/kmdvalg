# References

* [https://www.statsilk.com/maps/convert-esri-shapefile-map-geojson-format](https://www.statsilk.com/maps/convert-esri-shapefile-map-geojson-format)
* [https://help.github.com/articles/mapping-geojson-files-on-github/](https://help.github.com/articles/mapping-geojson-files-on-github/)
* [https://www.datavizforall.org/transform/mapshaper/](https://www.datavizforall.org/transform/mapshaper/)
* [https://github.com/mbloch/mapshaper/issues/194](https://github.com/mbloch/mapshaper/issues/194)
* [https://github.com/mbloch/mapshaper/wiki/Command-Reference](https://github.com/mbloch/mapshaper/wiki/Command-Reference)
* [http://spatialreference.org/ref/epsg/wgs-84-utm-zone-32n/](http://spatialreference.org/ref/epsg/wgs-84-utm-zone-32n/)
* [https://stackoverflow.com/questions/3149112/how-can-i-get-proj4-details-from-the-shapefiles-prj-file](https://stackoverflow.com/questions/3149112/how-can-i-get-proj4-details-from-the-shapefiles-prj-file)
* [https://gis.stackexchange.com/questions/7608/shapefile-prj-to-postgis-srid-lookup-table/7615#7615](https://gis.stackexchange.com/questions/7608/shapefile-prj-to-postgis-srid-lookup-table/7615#7615)


# Install mapshaper and gdal


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

# Python
conda create --yes -c conda-forge -n OSMNX python=3.6 osmnx gdal
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

## Find input coordinate system manully
On [https://mygeodata.cloud/cs2cs/](https://mygeodata.cloud/cs2cs/), in '**Chose input coordinate system**' we search for **ETRS89 / UTM zone 32N**.

This gives **EPSG=25832** and Proj.4 text

```
+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs
```

## Find input coordinate system with python and GDAL

```
# Activate conda environment
source activate OSMNX

# Read
IN=Kommune_DAGI_1_2mio
gdalsrsinfo ${IN}.prj -o all
gdalsrsinfo ${IN}.prj -o PROJ4

'+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs '

# Try with python
python -c "from osgeo import osr;p=open('${IN}.prj', 'r').read();s=osr.SpatialReference();s.ImportFromESRI([p]);print(s.ExportToProj4())"

'+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs'
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

# Define coordinate system FROM
#FROM="+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
FROM="+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs"

# Define coordinate system TO of merc coordinates
TO_MERC="+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 
+y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs"

# Define coordinate system TO of longlat coordinates
TO_LL="+proj=longlat +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 
+y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs"
```

Now convert

```
# Convert: merc
mapshaper ${IN}.shp -simplify dp 20% -proj $TO_MERC from=$FROM -o format=geojson ${IN}_merc.geojson

# Convert: merc
mapshaper ${IN}.shp -simplify dp 20% -proj $TO_LL from=$FROM -o format=geojson ${IN}_longlat.geojson
```

Test with EPSG codes

```
IN=Kommune_DAGI_1_2mio
TO_EPSG="+proj=longlat +init=EPSG:3857"
FROM_EPSG="+init=EPSG:25832"

mapshaper ${IN}.shp -simplify dp 20% -proj $TO_EPSG from=$FROM_EPSG -o format=geojson ${IN}_EPSG.geojson
```

Afterwards test the .geojson file with **mapshaper-gui**

```
mapshaper-gui
```

[Github map](https://github.com/tlinnet/kmdvalg/tree/master/examples/Data/DAGI_Kommunal_1_2mio_kortforsyningen)