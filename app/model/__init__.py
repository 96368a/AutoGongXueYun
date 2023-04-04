from peewee import *

db = SqliteDatabase('data.db')

db.connect()