'use strict';
import $ from 'jquery'

import './lib/oms.min'

import filter from './filter'
import colorUtils from './colors'
import template from './popup'

class Visualization {

  /**
   * Creates a new visualization
   * @param  {L.Map}          map     The Leaflet map to add the visualization to
   * @param  {Arrray[Object]} data    The complete list of incidents to visualize
   * @param  {Array[String]}  colors  The colors to be used in HEX format
   * @constructor
   */
  constructor (map, data, colors) {
    this.map = map
    this.data = data
    this.colors = colors

    // set up OMS
    this.oms = new OverlappingMarkerSpiderfier(map, {
      keepSpiderfied: true,
      nearbyDistance: 1
    })

    this.oms.legColors = {
      usual: 'rgba(0,0,0,.2)',
      highlighted: 'rgba(0,0,0,.6)'
    }

    var popup = new L.Popup({
      autoPanPadding: [96, 96],
      closeButton: false,
      maxHeight: 250
    });
    this.oms.addListener('click', function (marker) {
      if (map.getZoom() < 10)
        map.setZoom(9)

      popup.setContent(template(marker.incident))
      popup.setLatLng(marker.getLatLng())
      map.openPopup(popup)
    })

    // set up markers
    this._markers = new Map()
    this.setupMarkers()
  }

  /**
   * Gets all currently active categories
   * @return {Array[string]}
   */
  getActiveCategories () {
    var activeCategories = []
    this._$categoryList.children().each(function () {
      var $li = $(this)
      if ($li.hasClass('active'))
        activeCategories.push($li[0].classList[0])
    })

    return activeCategories
  }

  /**
   * Sets up the category filter
   * @param  {jQuery.Selector} selector The container holding the LIs
   *                                    representing the different categories
   * @return {Visualization}
   * @chainable
   */
  setupCategoryFilter (selector) {
    this._$categoryList = $(selector)

    this._$categoryList.on('click', 'a', e => {
      $(e.target).parent().toggleClass('active')

      var incidents = this.filterAll()
      this.displayMarkers(incidents)

      e.preventDefault()
      e.stopPropagation()
      return false
    })

    return this
  }

  /**
   * Get currently active year
   * @return {String}
   */
  getCurrentYear () {
    return this._$yearList.children('.active').find('a').data().showYear
  }

  /**
   * Creates the year list which optionally already holds a button for "all"
   * @param  {jQuery.Selector} selector The container holding
   * @return {Visualization}
   * @chainable
   */
  setupYearFilter (selector) {
    var fragment = document.createDocumentFragment()
    var $a = $(document.createElement('a')).attr('href', '#')
    var $li = $(document.createElement('li')).append($a)

    this._$yearList = $(selector)

    var years = new Set()
    this.data.forEach(incident => { years.add(incident.date.substr(0, 4)) })

    Array.from(years).sort().forEach(function (year) {
      $li.clone()
        .find('a')
        .text(year)
        .data({ showYear: year })
        .end()
        .appendTo(fragment)
    })

    this._$yearList
      .prepend(fragment)
      .on('click', 'a', e => {
        var $target = $(e.target)
        $target.parent().siblings().removeClass('active')
        $target.parent().addClass('active')

        var incidents = this.filterAll()
        this.displayMarkers(incidents)

        e.preventDefault()
        e.stopPropagation()
        return false
      })

    return this
  }

  filterAll () {
    var year = this.getCurrentYear()
    var categories = this.getActiveCategories()

    var byYear = (year) ? filter.byYear(this.data, year) : this.data
    return filter.byCategories(byYear, categories)
  }

  /**
   * Sets up all markers for the first time so afterwards they only need to be
   * faded in and out
   * @return {Visualization}
   * @chainable
   */
  setupMarkers () {
    this.data.forEach(incident => {
      var icon = L.divIcon({
        className: 'circle-marker',
        iconSize: [18, 18]
      })

      var options = { icon: icon }
      var marker = L.marker([incident.lat, incident.lng], options)
        .addTo(this.map)

      marker.incident = incident

      var color = colorUtils.hexToRGB(this._pickColor(incident))
      $(marker._icon).css({
        borderColor: `rgba(${color[0]},${color[1]},${color[2]},.5)`,
        backgroundColor: `rgba(${color[0]},${color[1]},${color[2]},.2)`
      })

      this.oms.addMarker(marker)
      this._markers.set(incident, marker)
    })

    return this
  }

  /**
   * Clear the map and render new markers
   * @param  {Array[Object]} incidents The incidents to be shown
   * @return {Visualization}
   * @chainable
   */
  displayMarkers (incidents) {
    if (incidents == null)
      incidents = this.data

    for (var [incident, marker] of this._markers)
      if (incidents.indexOf(incident) == -1) {
        $(marker._icon).hide()
        this.oms.removeMarker(marker)
      } else {
        $(marker._icon).show()
        this.oms.addMarker(marker)
      }

    return this
  }

  /**
   * Picks a color for a given incident based on its categories
   * @param  {Object} incident A single incident
   * @return {String}          A color as HEX string
   */
  _pickColor (incident) {
    var categories = ['racism', 'antisemitism', 'sexism', 'homophobia']
      .map(function (category, index) {
        if (incident.categories.indexOf(category) !== -1)
          return index
      }).filter(function (value) {
        return value != null
      })

    var categoryColors = this.colors.filter(function (color, index) {
      return categories.indexOf(index) !== -1
    })

    return incident.categories.length ? colorUtils.mix(categoryColors) : this.colors[4]
  }

}

export default Visualization
