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

# Set up the tables
def create_tables():
    db.connect()
    db.create_tables([Article])
