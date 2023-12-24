## factories.py
import factory
from factory.django import DjangoModelFactory
from main.models import *

## Defining a factory
class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker("name")
    address = factory.Faker("address")
    city = factory.Faker("city")
    country = factory.Faker("country")


class PublisherFactory(DjangoModelFactory):
    class Meta:
        model = Publisher

    name = factory.Faker("sentence", nb_words=2)
    address = factory.Faker("address")
    city = factory.Faker("city")
    state_province = country = factory.Faker("state")
    country = factory.Faker("country")

class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=4)
    abstract = factory.Faker("sentence", nb_words=50)
    author = factory.Iterator(Author.objects.all())
    publisher = factory.Iterator(Publisher.objects.all())
    publication_date = factory.Faker("date_time")


