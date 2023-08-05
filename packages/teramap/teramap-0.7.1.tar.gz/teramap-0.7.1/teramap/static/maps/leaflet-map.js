import L from 'leaflet';

// we assume the resulting teramap.js is consumed using the bundle
// with leaflet loaded externally.
// can be replaced with externals options if this is merged:
// https://github.com/webpack-contrib/css-loader/pull/496
// import 'leaflet/dist/leaflet.css';

// make sure Leaflet's images work properly:
// delete L.Icon.Default.prototype._getIconUrl;
// L.Icon.Default.mergeOptions({
//     iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
//     iconUrl: require('leaflet/dist/images/marker-icon.png'),
//     shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
// });


import 'leaflet-fullscreen';
import 'leaflet-fullscreen/dist/leaflet.fullscreen.css';

import {class as GeocoderControl} from 'leaflet-control-geocoder/src/control.js';
import 'leaflet-control-geocoder/Control.Geocoder.css';

import preventAccidentalScroll from '../lib/leaflet-scroll-intent.js';

import MiniMap from 'leaflet-minimap';
import 'leaflet-minimap/src/Control.MiniMap.css';

function leaflet_map(map_id, options) {
    options = L.extend({
        center: [51, 4],
        zoom: 6,
        callback: L.Util.falseFn,
        // name -> L.TileLayer mapping of base layers. to add to the layers control.
        baselayers: {
            'map': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                'minZoom': 1,
                'maxZoom': 19,
                'attribution': '&copy; OpenStreetMap',
            })
        },
        // name -> L.TileLayer mapping of overlays to add to the layers control.
        overlays: {},
        // plugins to activate or not:
        preventAccidentalScroll: true,
        fullscreenControl: true,
        searchControl: false,
        minimap: false,
        // default options for the Layers Control. Set to false to disable layers control.
        layersControlOptions: {
            collapsed: false
        }
    }, options || {});

    // allow passing a single tile layer.
    if (options.baselayers instanceof L.TileLayer) {
        options.baselayers = {
            'default': options.baselayers
        };
    }
    map_id = L.DomUtil.get(map_id);
    L.DomUtil.addClass(map_id, 'teramap');

    var map = L.map(map_id).setView(options.center, options.zoom);
    // attach map container to data attribute of DOM element
    map._container.data = map;

    map.addLayer(options.baselayers[Object.keys(options.baselayers)[0]]);

    if (options.layersControlOptions && (Object.keys(options.baselayers).length > 1 || Object.keys(options.overlays).length > 0)) {
        map.layersControl = L.control.layers(options.baselayers, options.overlays, options.layersControlOptions);
        map.layersControl.addTo(map);
    }
    if (options.fullscreenControl) {
        map.fullscreenControl = L.control.fullscreen();
        map.fullscreenControl.addTo(map);
    }
    if (options.searchControl) {
        new GeocoderControl().addTo(map);
    }
    if (options.preventAccidentalScroll) {
        preventAccidentalScroll(map);
    }
    if (options.minimap !== false) {
        if (!options['minimapLayer']) {
            options['minimapLayer'] = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png');
        }
        new MiniMap(options['minimapLayer'], options.minimap).addTo(map);
    }

    if (typeof options.callback == 'function') {
        options.callback(map);
    }

    return map;
}

export default leaflet_map;
