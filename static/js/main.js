(function () {
  "use strict";

  // set up background map
  var map = L.map('map').setView([52.50, 13.40], 11);
  var layer = new L.StamenTileLayer('toner-lite');
  map.addLayer(layer);

  // get response from server and draw the map
  var response;
  $.getJSON('/articles/')
    .fail(console.error.bind(console))
    .then(function (data) {
      console.log('Got data successfully!');
      response = data;

      displayAll();
    });

  // logic for drawing follows

  var markers = [];

  /**
   * Display all incidents at once
   */
  function displayAll () {
    for (var i = 0, l = response.length; i < l; i++) {
      markers.push(
        L.marker([response[i].lat, response[i].lng]).addTo(map).bindPopup(response[i].description)
      )
    }
  }
})();
