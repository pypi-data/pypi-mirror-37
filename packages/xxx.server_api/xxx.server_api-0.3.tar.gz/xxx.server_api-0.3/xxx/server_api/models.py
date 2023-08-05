from couchdb_schematics.document import SchematicsDocument
from datetime import datetime
from schematics.models import Model
from schematics.types import (
    BooleanType,
    DateTimeType,
    IntType,
    ListType,
    StringType,
    URLType,
)
from schematics.types.compound import ModelType


class Image(Model):
    source = URLType(max_length=100)
    link = StringType(max_length=100)

    def __eq__(x, y):
        return x.link == y.link

    def __hash__(self):
        return hash(self.link)


class Post(Model):
    age = IntType()
    city = StringType(max_length=50)
    date_post = DateTimeType()
    description = StringType(max_length=3000)
    height = IntType()
    images = ListType(ModelType(Image), default=list())
    images_scraped = BooleanType(default=False)
    title = StringType(max_length=255)
    name = StringType(max_length=25)
    url_link = URLType(max_length=200)
    weight = IntType()


class Number(SchematicsDocument, Model):
    _id = StringType()
    _rev = StringType()
    age = IntType()
    images_scraped = BooleanType(default=False)
    last_post_date = DateTimeType()
    name = StringType(max_length=25)
    posts = ListType(ModelType(Post), default=list())




