from peewee import *
from app.model import db

class Log(Model):
    content = CharField()
    userId = CharField()
    time = DateTimeField()

    class Meta:
        database = db  # This model uses the "people.db" database.
        
db.create_tables([Log,])