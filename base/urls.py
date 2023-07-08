from django.urls import path, include
from .views import *
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'companies', CompanyViewSet)

urlpatterns = [
    # path('api/', include(router.urls)),
    path('getcompanies/', get_company),
    path('postcompanies/', post_company)
]
