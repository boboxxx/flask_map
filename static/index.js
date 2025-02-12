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
// 初始化地图
var map = L.map('map').setView([39.916611, 116.390748], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// 初始化变量
var socket = io.connect();
var cars = {};
var heatmapLayer = null;
var bounds = L.latLngBounds();

// 监听服务器数据
socket.on('device_data', function(data) {
    console.log(data);
    setCar(data);
    updateVehicleList(data);
});

// 更新车辆列表
function updateVehicleList(data) {
    if (!data) return;
    
    var carNumber = Object.keys(data)[0];
    var carPosition = data[carNumber];
    var vehicleList = document.getElementById('vehicleList');
    
    // 检查是否已存在该车辆的列表项
    var existingItem = document.getElementById(carNumber + '-item');
    if (!existingItem) {
        var li = document.createElement('li');
        li.id = carNumber + '-item';
        li.className = 'vehicle-item';
        li.style.cursor = 'pointer';
        li.innerHTML = `
            <div>
                <span class="vehicle-status ${carPosition.flag ? 'status-active' : 'status-inactive'}"></span>
                <strong>${carNumber}</strong>
            </div>
            <div class="mt-2">
                <small>Latitude: ${carPosition.latitude}</small><br>
                <small>Longitude: ${carPosition.longitude}</small>
            </div>
        `;
        // 添加点击事件处理器
        li.addEventListener('click', function() {
            if (cars[carNumber]) {
                var marker = cars[carNumber].marker;
                var position = marker.getLatLng();
                map.setView(position, 15);
                marker.openPopup();
            }
        });
        vehicleList.appendChild(li);
    } else {
        // 更新现有列表项的信息
        existingItem.innerHTML = `
            <div>
                <span class="vehicle-status ${carPosition.flag ? 'status-active' : 'status-inactive'}"></span>
                <strong>${carNumber}</strong>
            </div>
            <div class="mt-2">
                <small>Latitude: ${carPosition.latitude}</small><br>
                <small>Longitude: ${carPosition.longitude}</small>
            </div>
        `;
        // 更新点击事件处理器
        existingItem.onclick = function() {
            if (cars[carNumber]) {
                var marker = cars[carNumber].marker;
                var position = marker.getLatLng();
                map.setView(position, 15);
                marker.openPopup();
            }
        };
    }
}

function setCar(data) {
    if (!data) return;
    
    var carNumber = Object.keys(data)[0];
    var carPosition = data[carNumber];
    var latlng = [carPosition.latitude, carPosition.longitude];
    
    // 创建更醒目的自定义图标
    var carIcon = L.divIcon({
        html: '<i class="fas fa-car" style="color: #FF0000; font-size: 24px;"></i>',
        className: 'vehicle-icon',
        iconSize: [40, 40],
        iconAnchor: [20, 20],
        popupAnchor: [0, -20]
    });
    
    if (!(carNumber in cars)) {
        // 创建新的车辆对象，只包含标记点
        cars[carNumber] = {
            marker: L.marker(latlng, {icon: carIcon}).addTo(map)
        };
        
        // 添加弹出信息
        cars[carNumber].marker.bindPopup(`
            <div class="popup-content">
                <h6>${carNumber}</h6>
                <p>Status: ${carPosition.flag ? 'Active' : 'Inactive'}</p>
                <p>Location: ${latlng.join(', ')}</p>
            </div>
        `);
        
        // 更新边界
        bounds.extend(latlng);
    } else {
        // 只更新现有车辆位置
        cars[carNumber].marker.setLatLng(latlng);
        bounds.extend(latlng);
    }
}

// 显示所有车辆
function fitAllMarkers() {
    if (!bounds.isValid()) return;
    map.fitBounds(bounds, {padding: [50, 50]});
}

// 切换热力图
function toggleHeatmap() {
    if (heatmapLayer) {
        map.removeLayer(heatmapLayer);
        heatmapLayer = null;
    } else {
        var heatData = [];
        Object.values(cars).forEach(car => {
            var pos = car.marker.getLatLng();
            heatData.push([pos.lat, pos.lng, 1]);
        });
        heatmapLayer = L.heatLayer(heatData, {radius: 25}).addTo(map);
    }
}

// 生成随机颜色
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
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