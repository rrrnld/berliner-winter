(function () {
  var map = L.map('map').setView([52.50, 13.40], 11);
  var layer = new L.StamenTileLayer("toner-lite");
  map.addLayer(layer);
})();
