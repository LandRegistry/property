//Define coordinate system using PROJ4 standards
var osgb = new L.Proj.CRS('EPSG:27700',
  '+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000' +
  '+ellps=airy +datum=OSGB36 +units=m +no_defs',
  {
    resolutions: [2500, 1000, 500, 200, 100, 50, 25, 10, 5, 2.5, 1],
    bounds: L.bounds([1300000,0],[700000,0])
  }
);

//Leaflet map with OS options
var map = new L.Map('map', {
  crs: osgb,
  continuousWorld: true,
  worldCopyJump: false,
  minZoom: 1,
  maxZoom: 10,
});

//New OSOpenSpace layer with API Key
openspaceLayer = L.tileLayer.osopenspace("FFB702322FE0714DE0430B6CA40A06C6", {debug: true});
map.addLayer(openspaceLayer);

map.setView([51.504, -0.159], 9);

//Define name of CRS in GeoJSON using PROJ4
proj4.defs("urn:ogc:def:crs:EPSG:27700","+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +datum=OSGB36 +units=m +no_defs");

//The GeoJSON object, hard coded now but would be parameterised or Jinja-fied
//A polygon around Lincolns Inn Fields, London.
var geojson = {
    "type": "Feature",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:EPSG:27700"
        }
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    404439.5558898761,
                    369899.8484076261
                ],
                [
                    404440.0558898761,
                    369899.8484076261
                ],
                [
                    404440.0558898761,
                    369900.3484076261
                ],
                [
                    404439.5558898761,
                    369900.3484076261
                ],
                [
                    404439.5558898761,
                    369899.8484076261
                ]
            ]
        ]
    },
    "properties": {
        "Description": "Polygon"
    }
};

//Add the GeoJSON to the map
L.Proj.geoJson(geojson).addTo(map);

//Add a scale control to the map
L.control.scale().addTo(map);
