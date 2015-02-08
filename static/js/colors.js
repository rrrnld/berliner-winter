var colorUtils = {

  /**
   * Converts a hex string to RGB
   * @param  {String}        color A string in six digit hex format
   * @return {Array[Number]}       An array of 3 integers which are the red,
   *                               green and blue values
   */
  hexToRGB: function toRGB (color) {
    var r = color.substr(1, 2)
      , g = color.substr(3, 2)
      , b = color.substr(5, 2);

    return [parseInt(r, 16), parseInt(g, 16), parseInt(b, 16)];
  },

  /**
   * Mixes an arbitrary amount of colors linearly
   * @param  {Array[String]} colors Different colors as hex string
   * @return {String}               The mixed color as hex string
   */
  mix: function mixColors (colors) {
    var rgb = colors.map(colorUtils.hexToRGB);

    var result = [ 0, 0, 0 ];
    for (var i = 0, l = rgb.length; i < l; i++) {
      result[0] += rgb[i][0] / l;
      result[1] += rgb[i][1] / l;
      result[2] += rgb[i][2] / l;
    }

    return '#' + result[0].toString(16) + result[1].toString(16) + result[2].toString(16);
  }

}

export default colorUtils;
