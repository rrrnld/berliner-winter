'use strict';
import $ from 'jquery'
import filter from './filter'
import colorUtils from './colors'

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

    this._markers = []
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

      var categories = this.getActiveCategories()
      var incidents = filter.byCategories(this.data, categories)
      this.displayMarkers(incidents)

      e.preventDefault()
      e.stopPropagation()
      return false
    })

    return this
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

        var year = $target.data().showYear
        var incidents = (year) ? filter.byYear(this.data, year) : this.data

        this.displayMarkers(incidents)

        e.preventDefault()
        e.stopPropagation()
        return false
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

    this._markers.forEach(marker => { this.map.removeLayer(marker) })
    this._markers = incidents.map(incident => {
      return this._createMarker(incident).bindPopup(incident.description.replace(/\n/g, '<br>'))
    })

    return this
  }

  /**
   * Creates the correct marker for a single incident and adds it to the map
   * @param  {Object}         data A single incident
   * @return {L.CircleMarker}
   */
  _createMarker (data) {
    var options =  { color: this._pickColor(data) }
    var marker = L.circleMarker([data.lat, data.lng], options).addTo(this.map)
    return marker
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
