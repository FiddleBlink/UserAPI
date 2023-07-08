from django.urls import path, include
from .views import *
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'companies', CompanyViewSet)

urlpatterns = [
    # path('api/', include(router.urls)),
    path('get_company/', get_company),
    path('post_company/', post_company),
    path('update_company/<str:pk>/', update_company),
    path('delete_company/<str:pk>/', delete_company),
]
