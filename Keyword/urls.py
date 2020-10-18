from django.urls import path

from Keyword import views

urlpatterns = [
    path('phrase/', views.key_phrase),
    path('wgt/', views.weight_phrase),
    path('weight/', views.weight),
    path('keyword/', views.keyword),
    path('test/', views.test),
]