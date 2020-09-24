import mongoengine
from django.db import models

# Create your models here.
from mongoengine import *

class Text(Document):
    text = StringField(required=True)
    words = ListField(StringField())
    tfidf = ListField()
    keyword = ListField()

class Review(Document):
    text = StringField(required=True)
    words = ListField(StringField())
    tfidf = ListField()
    keyword = ListField()