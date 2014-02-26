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
var activeLocation = null;

function openFeatureDiv(location) {
    activeLocation = location;

    var form = document.forms['featureForm'];
    form['name'].value = location.attributes.name;
    form['address'].value = location.attributes.address;
    form['notes'].value = location.attributes.notes;

    featureDiv.style.visibility = "visible";
}

function resetFeatureDiv() {
    openFeatureDiv(activeLocation);
}

function closeFeatureDiv() {
    featureDiv.style.visibility = "hidden";
}

function saveFeature() {
    // TODO
    alert("TODO");
}


popupControl = new OpenLayers.Control.SelectFeature(locs, {
    onSelect: openFeatureDiv
});
map.addControl(popupControl);
popupControl.activate();
