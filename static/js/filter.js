export default {

  /**
   * Returns only the incidents which fall into the given categories
   * @param  {Array[Object]} data The incidents to filter
   * @param  {Array[String]} categories
   * @return {Array[Obect]}
   */
  byCategories: function (data, categories) {
    return data.filter(function (incident) {
      for (var i = 0, l = incident.categories.length; i < l; i++)
        if (categories.indexOf(incident.categories[i]) !== -1)
          return true

      return false
    });
  },

  /**
   * Return only the incidents that happened in a given year
   */
  byYear: function (data, year) {
    return data.filter(function (incident) {
      return incident.date.indexOf(year) === 0
    })
  }

};
