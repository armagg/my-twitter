from django.shortcuts import render


def get_alerts(request):
    user_id = request.user.id
