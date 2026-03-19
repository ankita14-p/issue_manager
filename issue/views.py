from django.shortcuts import render,redirect
from .models import Issue,Comment
from vendors.models import Vendor
from django.contrib.auth.decorators import login_required
from .forms import IssueForm
from notifications.models  import Notification
from django.http import JsonResponse
@login_required
def dashboard(request):

    issues = Issue.objects.all().order_by('-created_at')
    status = request.GET.get('status')

    if status:
        issues = issues.filter(status=status)

    severity = request.GET.get('severity')
    assignee = request.GET.get('assignee')
    search = request.GET.get('search')

    if severity:
        issues = issues.filter(severity=severity)

    if assignee:
        issues = issues.filter(assigned_to__id=assignee)

    if search:
        issues = issues.filter(title__icontains=search)

    total = Issue.objects.count()
    open_count = Issue.objects.filter(status='Open').count()
    progress = Issue.objects.filter(status='In Progress').count()
    resolved = Issue.objects.filter(status='Resolved').count()
    low=Issue.objects.filter(severity='Low').count()
    high=Issue.objects.filter(severity="High").count()
    medium=Issue.objects.filter(severity="Medium").count()
    critical= Issue.objects.filter(severity="Critical").count()

    vendors = Vendor.objects.all()

    form = IssueForm()

    return render(request,'dashboard.html',{
        'issues':issues,
        'total':total,
        'open':open_count,
        'progress':progress,
        'resolved':resolved,
        'vendors':vendors,
        'form':form,
        'low':low,
        'medium':medium,
        'high':high,
        'critical':critical
    })

@login_required
def create_issue(request):

    if request.method == "POST":

        form = IssueForm(request.POST, request.FILES)

        if form.is_valid():

            issue = form.save(commit=False)

            # creator
            issue.created_by = request.user

            # assign vendor
            vendor_id = request.POST.get("assigned_to")

            if vendor_id:
                issue.assigned_to = Vendor.objects.get(id=vendor_id)

            # attachment
            if 'attachment' in request.FILES:
                issue.attachment = request.FILES['attachment']

            issue.save()
            Notification.objects.create(
             user=request.user,
             issue=issue,
            type="issue_created",
            message=f"New issue created: {issue.title}"
)

            return redirect("dashboard")

        else:
            print(form.errors)

    return redirect("dashboard")

@login_required
def delete_issue(request,id):

    issue = Issue.objects.get(id=id)

    Notification.objects.create(
        user=request.user,
        issue=issue,
        type="issue_deleted",
        message=f"Issue deleted: {issue.title}"
    )

    issue.delete()

    return redirect('dashboard')

@login_required
def update_status(request):

    if request.method == "POST":

        try:
            issue = Issue.objects.get(id=request.POST['id'])
            issue.status = request.POST['status']
            issue.save()

            Notification.objects.create(
                user=request.user,
                issue=issue,
                type="status_updated",
                message=f"Status updated to {issue.status} for issue: {issue.title}"
            )

            return JsonResponse({'success':True})

        except:
            return JsonResponse({'success':False})
@login_required
def issue_detail(request,id):

    issue = Issue.objects.get(id=id)

    comments = Comment.objects.filter(issue=issue)

    if request.method == "POST":

        comment = Comment.objects.create(
            issue=issue,
            user=request.user,
            text=request.POST["comment"]
        )

        Notification.objects.create(
            user=request.user,
            issue=issue,
            type="comment_added",
            message=f"{request.user.username} commented on {issue.title}"
        )

        return redirect("issue_detail",id=id)

    return render(request,"issue_detail.html",{
        "issue":issue,
        "comments":comments
    })
@login_required
def board(request):

    vendor_id = request.GET.get("vendor")

    open_issues = Issue.objects.filter(status="Open")
    progress_issues = Issue.objects.filter(status="In Progress")
    resolved_issues = Issue.objects.filter(status="Resolved")

   
    if vendor_id:
        open_issues = open_issues.filter(assigned_to__id=vendor_id)
        progress_issues = progress_issues.filter(assigned_to__id=vendor_id)
        resolved_issues = resolved_issues.filter(assigned_to__id=vendor_id)

    open_issues = open_issues.order_by("-created_at")
    progress_issues = progress_issues.order_by("-created_at")
    resolved_issues = resolved_issues.order_by("-created_at")

    vendors = Vendor.objects.all()

    context = {
        "open_issues": open_issues,
        "progress_issues": progress_issues,
        "resolved_issues": resolved_issues,

        "open_count": open_issues.count(),
        "progress_count": progress_issues.count(),
        "resolved_count": resolved_issues.count(),

        "vendors": vendors,
        "selected_vendor": vendor_id   
    }

    return render(request, "board.html", context)