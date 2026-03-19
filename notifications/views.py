from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from issue.models import Issue
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
# Create your views here.
@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    last7 = timezone.now() - timedelta(days=7)

    new_issues = Issue.objects.filter(created_at__gte=last7).count()

    unresolved = Issue.objects.exclude(status="Resolved").count()

    critical = Issue.objects.filter(severity="Critical").count()

    # mark as read only after loading
    Notification.objects.filter(user=request.user,is_read=False).update(is_read=True)

    return render(request,"notifications.html",{
        "notifications":notifications,
        "new_issues":new_issues,
        "unresolved":unresolved,
        "critical":critical
    })
@login_required
def notification_count(request):

    count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return JsonResponse({"count":count})
@login_required
def delete_notification(request, id):

    notification = Notification.objects.get(id=id, user=request.user)

    notification.delete()

    return redirect("notifications")