(function () {
  "use strict";

  // http://www.colourlovers.com/palette/1811244/1001_Stories
  var colors = [ '#F8B195', '#F67280', '#C06C84', '#6C5B7B', '#355C7D' ];

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
  function createMarker (data) {
    var options =  { color: pickColor(data) };
    var marker = L.circleMarker([data.lat, data.lng], options).addTo(map);
    return marker;
  }

  function pickColor (data) {
    var categories = [ 'racism', 'antisemitism', 'sexism', 'homophobia' ];
    return data.categories.length ? colors[categories.indexOf(data.categories[0])] : colors[4];
  }

  /**
   * Display all incidents at once
   */
  function displayAll () {
    for (var i = 0, l = response.length; i < l; i++) {
      markers.push(createMarker(response[i]).bindPopup(response[i].description));
    }
  }
})();
