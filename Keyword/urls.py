from django.urls import path

from Keyword import views

urlpatterns = [
    path('clean/', views.clean),
    path('count/', views.count),
    # path('test/', views.test),
]