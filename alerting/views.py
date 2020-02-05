from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from alerting.models import Alert


@login_required
def notifies(request):
    return render(request, 'alerting/alert.html', {'alerts': Alert.get_alerts(request.user.id)})
