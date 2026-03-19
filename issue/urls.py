from django.urls import path
from . import views
 
urlpatterns=[
path('issues/',views.dashboard,name="dashboard"),
path('create/',views.create_issue,name="create_issue"),
path('delete/<int:id>/',views.delete_issue,name="delete_issue"),
path('update_status/',views.update_status,name="update_status"),

path('issue/<int:id>/',views.issue_detail,name="issue_detail"),
path('board/',views.board,name="board"),
]