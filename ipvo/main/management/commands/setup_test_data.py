import random

from django.db import transaction
from django.core.management.base import BaseCommand

from main.models import *
from main.factory import (
    AuthorFactory,
   BookFactory,
    PublisherFactory
)

NUM_AUTHORS = 160
NUM_BOOKS = 2000
NUM_PUBL = 60

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Author, Book, Publisher]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        for _ in range(NUM_AUTHORS):
            author = AuthorFactory()

        for _ in range(NUM_PUBL):
            publisher = PublisherFactory()
            
        for _ in range(NUM_BOOKS):
            book = BookFactory()
            