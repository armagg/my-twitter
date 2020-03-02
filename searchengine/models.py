from django.db import models


# Create your models here.
from django.db.models import Q


class DocIndex(models.Model):
    key = models.CharField(max_length=100, db_index=True)
    value = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    @staticmethod
    def add_doc(doc: str, value, type):
        words = doc.split(' ')
        for word in words:
            if word != '':
                for word2 in word.split('\n'):
                    if word2 != '':
                        new_doc = DocIndex(key=word2, value=value, type=type)
                        new_doc.save()

    @staticmethod
    def search(word):
        return DocIndex.objects.filter(Q(key=word))
