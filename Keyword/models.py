import mongoengine
from django.db import models

# Create your models here.
from mongoengine import *

class Text(Document):
    text = StringField(required=True)
    words = ListField(StringField())
    tfidf = ListField()
    keyword = ListField()
    tf_idf = ListField()
    key_word = ListField()

class Review(Document):
    text = StringField(required=True)
    words = ListField(StringField())
    tfidf = ListField()
    keyword = ListField()

