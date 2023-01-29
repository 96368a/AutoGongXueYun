from peewee import *
from app.model import db

class Config(Model):
    phone = CharField()
    password = CharField()
    token = CharField(1024)
    userId = IntegerField()
    planId = CharField()
    enable = BooleanField()
    keepLogin = BooleanField()
    userAgent = CharField()
    country = CharField()
    province = CharField()
    city = CharField()
    area = CharField()
    address = CharField()
    longitude = CharField()
    latitude = CharField()
    plusplusKey = CharField()
    ServerChanKey = CharField()
    randomLocation = BooleanField()
    signCheck = BooleanField()
    desc = CharField()
    type = CharField()
    

    class Meta:
        database = db # This model uses the "people.db" database.
        
def init():
    db.connect()
    db.create_tables([Config,])
        
def create(phone, password, token, userId, planId, enable, keepLogin, userAgent, country, province, city, area, address, longitude, latitude, plusplusKey, ServerChanKey, randomLocation, signCheck, desc, type):
    config = Config.create(phone=phone, password=password, token=token, userId=userId, planId=planId, enable=enable, keepLogin=keepLogin, userAgent=userAgent, country=country, province=province, city=city, area=area, address=address, longitude=longitude, latitude=latitude, plusplusKey=plusplusKey, ServerChanKey=ServerChanKey, randomLocation=randomLocation, signCheck=signCheck, desc=desc, type=type)
    config.save()
    return config