<!DOCTYPE html>
<html>
<head>
    <title>Visualization of Hate Crime in Berlin</title>
    <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/style.css">
    <link href='http://fonts.googleapis.com/css?family=Lora' rel='stylesheet' type='text/css'>
</head>
<body>
    <nav id="filter-picker">
        <ul class="year-filter">
            <li><a href="#">2005</a></li>
            <li><a href="#">2006</a></li>
            <li><a href="#">2007</a></li>
            <li><a href="#">2008</a></li>
            <li><a href="#">2009</a></li>
            <li><a href="#">2010</a></li>
            <li><a href="#">2011</a></li>
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
    <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
    <script src="http://maps.stamen.com/js/tile.stamen.js?v1.3.0"></script>
    <script src="/static/js/main.js"></script>
</body>
</html>
