from peewee import *
from app.model import db


class Config(Model):
    phone = CharField()
    password = CharField()
    token = CharField(1024)
    userId = CharField()
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
    serverChanKey = CharField()
    randomLocation = BooleanField()
    signCheck = BooleanField()
    desc = CharField()
    type = CharField()

    class Meta:
        database = db  # This model uses the "people.db" database.



db.connect()
db.create_tables([Config,])


def create_or_update(phone, password, token, userId):
    config = Config.get_or_none(Config.phone == phone)
    #用户已经存在则更新
    if config is not None:
        config.password = password
        config.token = token
        config.userId = userId
        config.save()
        return config
    config = Config.create(phone=phone, password=password, token=token, userId=userId, planId="", enable=False, keepLogin=False, userAgent="", country="", province="", city="",
                           area="", address="", longitude="", latitude="", plusplusKey="", serverChanKey="", randomLocation=True, signCheck=True, desc="", type="android")
    config.save()
    return config
