from django.urls import path
from . import views 

urlpatterns = [
    # path('<int:pk>/',views.ProductDetailAPIView.as_view()),
    # path('<int:pk>/update/',views.ProductUpdateAPIView.as_view()),
    path('',views.FileHandleAPIView.as_view()),
    # path('categories/',views.CategoryListAPIView.as_view()),
    path('search/',views.ProductListAPIView.as_view()),
    path('list/',views.ProductAdminListAPIView.as_view()),
]