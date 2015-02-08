'use strict';
import Visualization from './visualization'

// http://www.colourlovers.com/palette/1811244/1001_Stories
var colors = [ '#F8B195', '#F67280', '#C06C84', '#6C5B7B', '#355C7D' ]

// set up background map
var map = L.map('map').setView([52.50, 13.40], 11)
var layer = new L.StamenTileLayer('toner-lite')
map.addLayer(layer)

// restrict viewable area
map.setMaxBounds(map.getBounds().pad(0.4))
map.options.minZoom = map.getZoom()

// get response from server and draw the map
var visualization
$.getJSON('/articles/')
  .fail(console.error.bind(console))
  .then(function (response) {
    console.log('Got data successfully!')
    console.log(response.length)
    visualization = new Visualization(map, response, colors)
      .setupCategoryFilter('.category-filter')
      .setupYearFilter('.year-filter')
      .displayMarkers()
  })

$('.begin').on('click', function (e) {
  $('#overlay')
    .fadeOut(700)
    .then(function() { $(this).remove() })

  e.preventDefault()
  e.stopPropagation()
  return false
})
