from peewee import *

db = SqliteDatabase('violence.db')

class BaseModel(Model):
    class Meta:
        database = db

class Article(BaseModel):
    """
    An article is a single incident as crawled from the reach-out webpage
    """
    date = DateField(index=True)
    month_only = BooleanField(default=False)
    place = CharField()
    description = TextField()
    hash = BlobField(index=True)

class Location(BaseModel):
    """
    A location describes the place an incident has happened
    """
    confidence = IntegerField()
    lat = DoubleField()
    lng = DoubleField()
    match = CharField()
    returned_place = CharField()
    article = ForeignKeyField(Article)

class Category(BaseModel):
    """
    Describes the category of an incident (e.g. sexism, racism, antisemitism etc)
    """
    name = CharField()
    article = ForeignKeyField(Article)

# Set up the tables
def create_tables():
    db.connect()
    db.create_tables([Article, Location, Category])
