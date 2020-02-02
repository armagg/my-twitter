from django.db import models

# Create your models here.
from accounting.models import Account


class Page(models.Model):
    title = models.CharField(max_length=1000, blank=True)
    creator = models.ForeignKey(Account, on_delete=models.PROTECT, null=True)
    admins = models.ManyToManyField(Account, related_name='pages')
    personal_page = models.BooleanField()
    public = models.BooleanField(default=True)
