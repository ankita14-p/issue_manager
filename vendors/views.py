from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Vendor
from issue.models import Issue
from django.db.models import Avg
# Create your views here.
@login_required
def vendors(request):

    search = request.GET.get("search","")

    vendors = Vendor.objects.all()

    if search:
        vendors = vendors.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(category__icontains=search) |
            Q(contact_person__icontains=search)
        )

    vendor_data = []

    for vendor in vendors:

        open_count = Issue.objects.filter(assigned_to=vendor,status="Open").count()
        progress_count = Issue.objects.filter(assigned_to=vendor,status="In Progress").count()
        resolved_count = Issue.objects.filter(assigned_to=vendor,status="Resolved").count()

        vendor_data.append({
            "vendor":vendor,
            "open":open_count,
            "progress":progress_count,
            "resolved":resolved_count
        })

    total_vendors = vendors.count()
    active_vendors = vendors.filter(status="Active").count()

    total_open_issues = Issue.objects.filter(status="Open").count()

    avg_rating = vendors.aggregate(avg=Avg("rating"))["avg"] or 0

    context = {
        "vendor_data":vendor_data,
        "total_vendors":total_vendors,
        "active_vendors":active_vendors,
        "total_open_issues":total_open_issues,
        "avg_rating":round(avg_rating,1),
        "search":search
    }

    return render(request,"vendors.html",context)
@login_required
def create_vendor(request):

    if request.method == "POST":

        try:
            Vendor.objects.create(
                name=request.POST.get("name"),
                category=request.POST.get("category"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                contact_person=request.POST.get("contact_person"),
                rating=float(request.POST.get("rating") or 0),
                status=request.POST.get("status")
            )

            return redirect("vendors")

        except Exception as e:
            print("ERROR:", e)   
            return redirect("vendors")

    return redirect("vendors")