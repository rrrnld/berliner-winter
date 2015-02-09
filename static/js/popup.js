export default function template(incident) {
  var html = ''
  var monthMap = {
    '01': 'Januar',
    '02': 'Februar',
    '03': 'März',
    '04': 'April',
    '05': 'Mai',
    '06': 'Juni',
    '07': 'Juli',
    '08': 'August',
    '09': 'September',
    '10': 'Oktober',
    '11': 'November',
    '12': 'Dezember',
  }

  var dateComponents = incident.date.split('-')
  var date = dateComponents[2] + '. ' + monthMap[dateComponents[1]] + ' ' + dateComponents[0]

  html += '<div data-id="' + incident.id + '">'
  html += '<h3 class="date">' + date + '</h3>'
  html += '<p>' + incident.description.replace(/\n/g, '<br>') + '</p>'
  html += '</div>'

  return html
}
