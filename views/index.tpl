<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <title>Berliner Winter - Rechte Übergriffe in Berlin 2005 bis 2014</title>
    <link href='http://fonts.googleapis.com/css?family=Libre+Baskerville:400,400italic,700' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/style.css">
</head>
<body>
    <script>document.body.classList.add('js')</script>
    <div id="overlay">
        <div class="text">
            <h1>Berliner Winter:</h1>
            <p>
                Jeder Punkt dieser Karte steht für einen Übergriff im Zeitraum von Januar 2005 bis November 2014.<br>
                Die Chronik wurde erstellt von <a href="http://reachoutberlin.de/" target="_blank">ReachOut Berlin</a>. Analyse und Visualisierung von Joshua Widmann und Arne Schlüter.
            </p>
            <a href="#" class="begin">Beginnen</a>
        </div>
    </div>
    <nav id="filter-picker">
        <ul class="year-filter">
            <li class="all active"><a href="#">Alle</a></li>
        </ul>

        <ul class="category-filter">
            <li class="racism active"><a href="#">Rassismus</a></li>
            <li class="antisemitism active"><a  href="#">Antisemitismus</a></li>
            <li class="sexism active"><a href="#">Sexismus</a></li>
            <li class="homophobia active"><a href="#">Homophobie</a></li>
            <li class="uncategorized active"><a href="#">Unkategorisiert</a></li>
        </ul>
    </nav>
    <div id="map"></div>

    <script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
    <script src="http://maps.stamen.com/js/tile.stamen.js?v1.3.0"></script>

    <script src="/static/jspm_packages/6to5-polyfill.js"></script>
    <script src="/static/jspm_packages/system.js"></script>
    <script src="/static/config.js"></script>
    <script>System.import('js/main');</script>
</body>
</html>
