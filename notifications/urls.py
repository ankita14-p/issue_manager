from django.urls import path
from . import views

urlpatterns=[
path("notifications/",views.notifications,name="notifications"),
path("notifications/count/",views.notification_count,name="notification_count"),
path("notification/delete/<int:id>/", views.delete_notification, name="delete_notification"),
]