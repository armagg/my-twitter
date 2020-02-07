from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from alerting.models import Alert


@login_required
def notifies(request):
    alerts = Alert.get_alerts(request.user.username)
    return render(request, 'alerting/alert.html', {'alerts': alerts})


def seen_alert(request, id):
    Alert.objects.filter(id=id).delete()
    return redirect('alerting:notifies')
