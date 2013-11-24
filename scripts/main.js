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
    })})
map.addLayer(locs)
