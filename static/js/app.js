document.getElementById('sidebar-toggle').addEventListener('click', function() {
	document.getElementById('sidebar').classList.toggle('hidden');
	setTimeout(function() {
		if (window.map) {
			window.map.invalidateSize();
		}
	}, 300);
});
