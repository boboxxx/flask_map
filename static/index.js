var cleanupClient = Client();


function Client() {
    var socket = io('ws://localhost:5000');

    socket.on('from-server', function (msg) {
        // var latlng = [msg.latitude, msg.longitude];

        // map.removeLayer(marker);

        // marker = L.marker(latlng).addTo(map);

        // car.addLatLng(latlng);
        console.log(msg);
    });

    return function cleanup() {
        socket.disconnect();
        console.log('Disconnected');
    };
}