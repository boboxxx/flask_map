setInterval(function() {
    fetch('/gps-data')
        .then(response => response.json())
        .then(data => {
            // 在这里处理GPS数据，例如更新地图标记
            console.log('Latitude:', data.latitude);
            console.log('Longitude:', data.longitude);
        });
}, 1000); 

