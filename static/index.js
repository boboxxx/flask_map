var map = L.map('map').setView([39.916611, 116.390748], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
var marker = L.marker([39.916611, 116.390748]).addTo(map);
var car = L.polyline([], {color: 'red'}).addTo(map);

setInterval(function() {
    fetch('/car1')
        .then(response => response.json())
        .then(data => {
            // var latlng = [msg.latitude, msg.longitude];

            // map.removeLayer(marker);

            // marker = L.marker(latlng).addTo(map);

            // car.addLatLng(latlng);
            // 在这里处理GPS数据，例如更新地图标记
            console.log('Latitude:', data.latitude);
            console.log('Longitude:', data.longitude);
        });
}, 2000); 

