from django.urls import path
from schedules import views

urlpatterns = [
    path("", views.ScheduleCrudApi.as_view()),
    path("test-webhook/", views.TestWebhookApi.as_view()),
]
