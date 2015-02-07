(function () {
  "use strict";

  // http://www.colourlovers.com/palette/1811244/1001_Stories
  var colors = [ '#F8B195', '#F67280', '#C06C84', '#6C5B7B', '#355C7D' ];

  // set up background map
  var map = L.map('map').setView([52.50, 13.40], 11);
  var layer = new L.StamenTileLayer('toner-lite');
  map.addLayer(layer);

  // restrict viewable area
  map.setMaxBounds(map.getBounds());
  map.options.minZoom = map.getZoom();

  // get response from server and draw the map
  var response;
  $.getJSON('/articles/')
    .fail(console.error.bind(console))
    .then(function (data) {
      console.log('Got data successfully!');
      response = data;

      displayMarkers(response);
    });

  // event handling / user interaction
  var $categoryList = $('.category-filter');

  function getActiveCategories ($li) {
    var activeCategories = [];
    $categoryList.children().each(function () {
      var $li = $(this);
      if ($li.hasClass('active'))
        activeCategories.push($li[0].classList[0])
    });

    return activeCategories;
  }

  $categoryList.on('click', 'a', function (e) {
    $(this).parent().toggleClass('active');

    var categories = getActiveCategories();
    var incidents = filterByCategories(categories);
    displayMarkers(incidents);

    e.preventDefault();
    e.stopPropagation();
    return false;
  })

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
   * Clear the map and render new markers
   * @param  {Array[Object]} data The incidents to be shown
   */
  function displayMarkers (incidents) {
    markers.forEach(function (marker) {
      map.removeLayer(marker);
    });
    markers = [];

    incidents.forEach(function (incident) {
      markers.push(createMarker(incident).bindPopup(incident.description));
    });
  }

  /**
   * Returns only the incidents which fall into the given categories
   * @param  {Array[String]} categories
   * @return {Arreay[Obect]}
   */
  function filterByCategories (categories) {
    return response.filter(function (incident) {
      for (var i = 0, l = incident.categories.length; i < l; i++)
        if (categories.indexOf(incident.categories[i]) !== -1)
          return true;

      return false;
    });
  }
})();
