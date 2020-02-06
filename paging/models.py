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
    description = models.CharField(max_length=1000, blank=True, default='')

    def get_all_admins(self):
        admins = self.admins.all()
        return admins

    def is_this_admin(self, account_id):
        is_admin = False
        for admin in self.admins:
            if admin.id is account_id:
                is_admin = True
                return True
        if not is_admin:
            return False
