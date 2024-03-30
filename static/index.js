// var data = {'car1':  [
//     {"latitude": 39.898457, "longitude": 116.391844, "flag":1},
//     {"latitude": 39.898595, "longitude": 116.377947, "flag":0},
//     {"latitude": 39.898341, "longitude": 116.368001, "flag":1},
//     {"latitude": 39.898063, "longitude": 116.357144, "flag":0},
//     {"latitude": 39.899095, "longitude": 116.351934, "flag":0},
//     {"latitude": 39.905871, "longitude": 116.35067, "flag":0},
//     {"latitude": 39.922329, "longitude": 116.3498, "flag":1}
// ],

// 'car2':[
//     {"latitude": 39.931017, "longitude": 116.349671, "flag": 0},
//     {"latitude": 39.939104, "longitude": 116.349225, "flag": 0},
//     {"latitude": 39.942233, "longitude": 116.34991, "flag": 0},
//     {"latitude": 39.947263, "longitude": 116.366892, "flag": 0},
//     {"latitude": 39.947568, "longitude": 116.387537, "flag": 1}
//   ]
// }
var map = L.map('map').setView([39.898457, 116.391844], 20); // 设置地图的初始视图

// 添加一个 OpenStreetMap 图层
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var socket = io.connect();
var cars = {};

socket.on('device_data', function(data) {
    console.log(data);
    setCar(data);
});

function setCar(data) {
    if (!data) {
        return;
    }
    var carNumber = Object.keys(data)[0];
    var carPosition = data[carNumber];
    if (!(carNumber in cars)) {
        // 如果车辆对象不存在，则创建新的车辆对象，然后创建标记和路径
        cars[carNumber] = {};
        cars[carNumber]['marker'] = L.animatedMarker([
            [carPosition.latitude, carPosition.longitude],
        ]).addTo(map);
        map.setView([carPosition.latitude, carPosition.longitude], 20);
    } else {
        // 如果车辆对象已存在，则更新标记的位置
        cars[carNumber]['marker'].setLatLng([carPosition.latitude, carPosition.longitude]);
        map.setView([carPosition.latitude, carPosition.longitude], 20);
    }
}

// 定义行驶轨迹路线
// var route1 = L.polyline([]).addTo(map);
// var route2 = L.polyline([]).addTo(map);


// var car1 = null;
// var car2 = null;
// var car1Popup = L.popup().setContent('Car 1');
// var car2Popup = L.popup().setContent('Car 2');
// function setCar(data) {
//     console.log(data);
//     if (!data) {
//         return;
//     } else {
//         if (car1 !== null) {
//             map.removeLayer(car1);
//         }
//         if (car2 !== null) {
//             map.removeLayer(car2);
//         }
//         if ('car1' in data && 'car2' in data) {
//             car1 = L.marker([data.car1.latitude, data.car1.longitude]).addTo(map);
//             car1.bindPopup(car1Popup).openPopup();
//             route1.addLatLng([data.car1.latitude, data.car1.longitude]);
//             car2 = L.marker([data.car2.latitude, data.car2.longitude]).addTo(map);
//             car2.bindPopup(car2Popup).openPopup();
//             route2.addLatLng([data.car2.latitude, data.car2.longitude]);
//         }
//         else if ('car1' in data) {
//             car1 = L.marker([data.car1.latitude, data.car1.longitude]).addTo(map);
//             car1.bindPopup(car1Popup).openPopup();
//             route1.addLatLng([data.car1.latitude, data.car1.longitude]);
//         } 
//         else if ('car2' in data) {
//             car2 = L.marker([data.car2.latitude, data.car2.longitude]).addTo(map);
//             car2.bindPopup(car2Popup).openPopup();
//             route2.addLatLng([data.car2.latitude, data.car2.longitude]);
//         } 
//         else {
//             console.log("error: no car data found.");
//         }
//     }
// }

// setInterval(function() {
//     fetch('/data')
//         .then(response => response.json())
//         .then(data => {
//             setCar(data);
//         });
// }, 1000); // 每秒请求一次数据