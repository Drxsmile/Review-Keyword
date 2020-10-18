import mongoengine
from django.db import models
# Create your models here.
from mongoengine import *


class Text(Document):
    text = StringField(required=True)
    keyword = ListField()


class Review(Document):
    text = StringField(required=True)
    keyword = ListField()


class Df(Document):
    df_dic = DynamicField()


class Tf(Document):
    tf_dic = DictField()
