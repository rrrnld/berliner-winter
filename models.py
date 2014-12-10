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
    additional_place = CharField(null=True)
    description = TextField()
    hash = BlobField(index=True)

# Set up the tables
def create_tables():
    database.connect()
    database.create_tables([Article])
