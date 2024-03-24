var map = L.map('map').setView([39.916611, 116.390748], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
var marker = L.marker([39.916611, 116.390748]).addTo(map);
var car = L.polyline([], {color: 'red'}).addTo(map);

var cleanupClient = Client(map, marker, car);


function Client(map, marker, car) {
    var socket = io('ws://localhost:50000');

    socket.on('from-server', function (msg) {
        debugger
        var latlng = [msg.latitude, msg.longitude];

        map.removeLayer(marker);

        marker = L.marker(latlng).addTo(map);

        car.addLatLng(latlng);
        console.log(msg);
    });

    return function cleanup() {
        socket.disconnect();
        console.log('Disconnected');
    };
}

