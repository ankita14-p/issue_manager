from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from issue.models import Issue
from vendors.models import Vendor
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone
# Create your views here.
@login_required
def analytics(request):

    total = Issue.objects.count()
    open_count = Issue.objects.filter(status='Open').count()
    progress = Issue.objects.filter(status='In Progress').count()
    resolved = Issue.objects.filter(status='Resolved').count()
    low=Issue.objects.filter(severity='Low').count()
    high=Issue.objects.filter(severity="High").count()
    medium=Issue.objects.filter(severity="Medium").count()
    critical= Issue.objects.filter(severity="Critical").count()

    severity_counts = {
        "Low": Issue.objects.filter(severity="Low").count(),
        "Medium": Issue.objects.filter(severity="Medium").count(),
        "High": Issue.objects.filter(severity="High").count(),
        "Critical": Issue.objects.filter(severity="Critical").count(),
    }

    assignee_data = {}

    vendors = Vendor.objects.all()

    for vendor in vendors:
        assignee_data[vendor.name] = Issue.objects.filter(assigned_to=vendor).count()

    # 7 Day Activity Trend

    last_week = timezone.now() - timedelta(days=7)

    created_data = (
        Issue.objects.filter(created_at__gte=last_week)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(count=Count("id"))
    )

    dates = []
    counts = []

    for item in created_data:
        dates.append(item["day"].strftime("%b %d"))
        counts.append(item["count"])

    context = {
        "total": total,
        "open": open_count,
        "progress": progress,
        "resolved": resolved,
        "low":low,
        "medium":medium,
        "high":high,
        "critical":critical,
        "severity_counts": severity_counts,
        "assignee_data": assignee_data,
        "trend_dates": dates,
        "trend_counts": counts
    }

    return render(request,"analytics.html",context)