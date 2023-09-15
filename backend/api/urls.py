from django.urls import path
from . import views

# localhost:8000/api/
urlpatterns = [
    path('',views.CustomAuthTokenView.as_view()),
]

