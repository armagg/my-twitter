from django.db import models


# Create your models here.
from django.db.models import Q


class DocIndex(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    @staticmethod
    def add_doc(doc: str, value, type):
        words = doc.split(' ')
        for word in words:
            if word is not '':
                new_doc = DocIndex(key=word, value=value, type=type)
                new_doc.save()

    @staticmethod
    def search(word):
        return DocIndex.objects.filter(Q(key=wo))
