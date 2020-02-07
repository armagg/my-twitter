from django.db import models

# Create your models here.
from accounting.models import Account
from paging.models import Page


class ConfirmRequest(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    channel = models.ForeignKey(Page, on_delete=models.CASCADE)
