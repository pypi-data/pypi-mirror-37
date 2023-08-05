/*
 * Modified from https://github.com/pointhi/leaflet-color-markers
 */

var colors = ['black', 'green', 'grey', 'orange', 'red', 'violet', 'yellow'];
var iconPath = require.context('./color-marker/', false);

module.exports = function colorIcon(color) {
    if (colors.indexOf(color) === -1) {
        return new L.Icon.Default();
    } else {
        var name = L.Util.template('./marker-icon-2x-{color}.png', {color: color});
        return new L.Icon({
            iconUrl: iconPath(name, true),
            shadowUrl: iconPath('./marker-shadow.png', true),
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            tooltipAnchor: [16, -28],
            shadowSize: [41, 41],
        });
    }
};
