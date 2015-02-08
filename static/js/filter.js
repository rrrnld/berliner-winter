export default {

  /**
   * Returns only the incidents which fall into the given categories
   * @param  {Array[Object]} data The incidents to filter
   * @param  {Array[String]} categories
   * @return {Array[Obect]}
   */
  categories: function (data, categories) {
    return data.filter(function (incident) {
      for (var i = 0, l = incident.categories.length; i < l; i++)
        if (categories.indexOf(incident.categories[i]) !== -1)
          return true

      return false
    });
  }

};
