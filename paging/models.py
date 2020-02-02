from django.db import models

# Create your models here.
from accounting.models import Account


class Page(models.Model):
    title = models.CharField(max_length=1000, blank=True)
    page_id = models.CharField(unique=True, max_length=100, blank=False, db_index=True, null=True)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    admins = models.ManyToManyField(Account, related_name='pages')
    personal_page = models.BooleanField()
    public = models.BooleanField(default=True)

    def get_all_admins(self):
        admins = self.admins.all()
        return admins
