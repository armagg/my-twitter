import random
import string

from django.db import models


class TokenManager(models.Model):
    username = models.TextField()
    code = models.TextField()
    type = models.TextField()

    @staticmethod
    def get_random_code():
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(20))

    @staticmethod
    def create_new_token(username, type):
        code = TokenManager.get_random_code()
        token = TokenManager(username=username, code=code, type=type)
        token.save()
        return token

    @staticmethod
    def create_new_token_for_activate(username):
        return TokenManager.create_new_token(username=username, type='activate')

    @staticmethod
    def create_new_token_for_reset_password(username):
        return TokenManager.create_new_token(username=username, type='reset')

    @staticmethod
    def is_valid_for_activate_account(code, delete):
        if TokenManager.objects.filter(code=code, type='activate'):
            if delete:
                TokenManager.objects.delete(code=code, type='activate')
            return True
        return False

    @staticmethod
    def get_username_of_this_code(code, delete):
        if not TokenManager.objects.filter(code=code, type='reset'):
            return None
        token = TokenManager.objects.get(code=code, type='reset')
        if delete:
            TokenManager.objects.delete(code=code, type='reset')
        return token.username
