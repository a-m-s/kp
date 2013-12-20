var map = new OpenLayers.Map({
    div: "map",
    layers: [
        new OpenLayers.Layer.OSM("OSM (without buffer)"),
        new OpenLayers.Layer.OSM("OSM (with buffer)", null, {buffer: 2})
    ],
    controls: [
        new OpenLayers.Control.Navigation({
            dragPanOptions: {
                enableKinetic: true
            }
        }),
        new OpenLayers.Control.PanZoom(),
        new OpenLayers.Control.Attribution()
    ],
    center: [0, 0],
    zoom: 3,
    projection: "EPSG:4326"
});

map.addControl(new OpenLayers.Control.LayerSwitcher());
map.addControl(new OpenLayers.Control.MousePosition({displayProjection: "EPSG:4326"}));

locs = new OpenLayers.Layer.Vector("Locations", {
    strategies: [new OpenLayers.Strategy.BBOX({resFactor: 1})],
    protocol: new OpenLayers.Protocol.HTTP({
	url: "api/v1.0/locations/",
	format: new OpenLayers.Format.GeoJSON()
    })});
map.addLayer(locs);

style = new OpenLayers.Style({
    graphicWidth: 21,
    graphicHeight: 25,
    graphicYOffset: -28,
    label: "${name}",
    externalGraphic: "http://openlayers.org/api/2.13.1/img/marker.png"
}, [
    // TODO: add real rules
]);
locs.styleMap = new OpenLayers.StyleMap(style);

//////////////////////////////////////////////////////////////////
// Location view and edit

var featureDiv = document.getElementById('featureDiv');
var featureName = document.getElementById('featureName');
var featureAddress1 = document.getElementById('featureAddress1');
var featureAddress2 = document.getElementById('featureAddress2');
var featureAddress3 = document.getElementById('featureAddress3');
var featureAddress4 = document.getElementById('featureAddress4');
var featureAddress5 = document.getElementById('featureAddress5');
var featureNotes = document.getElementById('featureNotes');

var activeLocation = null;

function openFeatureDiv(location) {
    activeLocation = location;
    featureName.innerHTML = location.attributes.name;
    featureAddress1.innerHTML = location.attributes.address[0];
    featureAddress2.innerHTML = location.attributes.address[1];
    featureAddress3.innerHTML = location.attributes.address[2];
    featureAddress4.innerHTML = location.attributes.address[3];
    featureAddress5.innerHTML = location.attributes.address[4];
    featureNotes.innerHTML = location.attributes.notes;
    featureDiv.style.visibility = "visible";
}

function resetFeatureDiv() {
    openFeatureDiv(activeLocation);
}

function closeFeatureDiv() {
    featureDiv.style.visibility = "hidden";
}


popupControl = new OpenLayers.Control.SelectFeature(locs, {
    onSelect: openFeatureDiv
});
map.addControl(popupControl);
popupControl.activate();
