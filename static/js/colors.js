export default function mixColors (colors) {
  var rgb = colors.map(function (color) {
    var r = color.substr(1, 2)
      , g = color.substr(3, 2)
      , b = color.substr(5, 2);

    return [parseInt(r, 16), parseInt(g, 16), parseInt(b, 16)];
  });

  var result = [ 0, 0, 0 ];
  for (var i = 0, l = rgb.length; i < l; i++) {
    result[0] += rgb[i][0] / l;
    result[1] += rgb[i][1] / l;
    result[2] += rgb[i][2] / l;
  }

  return '#' + result[0].toString(16) + result[1].toString(16) + result[2].toString(16);
}
