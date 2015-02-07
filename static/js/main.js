(function () {
  // set up background map
  var map = L.map('map').setView([52.50, 13.40], 11);
  var layer = new L.StamenTileLayer("toner-lite");
  map.addLayer(layer);

  $.get('/articles')
    .fail(console.error.bind(console))
    .then(function (data) {
      console.log('Got data successfully!');
      console.log(data);
    });
})();
