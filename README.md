# What is this?
A visualization of hate crime in Berlin, starting 2005.
The data is kindly provided by [ReachOut - Opferberatung und Bildung gegen Rechtsextremismus, Rassismus und Antisemitismus](http://www.reachoutberlin.de).
It is scraped regularly from their webpage and visualized and analyzed by software written by [Joshua Widmann](https://github.com/jshwdmnn) and [Arne Schlüter](https://github.com/aesthaddicts).

## How do I start?
In order to set up the tables you have to create them first. This is done quite easily using the `python` interpreter:
```python
from models import *
create_tables()
```

## Interesting statistics
1. How often did violence occur?
2. Where did it occur the most?
3. How do we categorize it?
4. How many did occur close train stations?