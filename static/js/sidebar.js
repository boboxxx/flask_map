document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const map = L.map('map').setView([51.505, -0.09], 13); // 替换为你的地图初始化代码

    // 监听侧边栏的显示/隐藏事件 (这里假设通过 CSS 类名 'collapsed' 来控制侧边栏的显示/隐藏)
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                // 等待一段时间，确保侧边栏动画完成后再更新地图大小
                setTimeout(function() {
                    map.invalidateSize();
                }, 300); // 300ms 是一个示例值，根据你的动画时长调整
            }
        });
    });

    // 监听侧边栏的 class 属性变化
    observer.observe(sidebar, {
        attributes: true
    });

    // 初始时也更新一次地图大小，防止初始状态下地图显示不正确
    map.invalidateSize();
});
