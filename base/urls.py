from django.urls import path, include
from .views import *
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'companies', CompanyViewSet)

urlpatterns = [

    ################################## API PATHS #################################
    # path('api/', include(router.urls)),
    # path('get_company/', get_company),
    # path('post_company/', post_company),
    # path('update_company/<str:pk>/', update_company),
    # path('delete_company/<str:pk>/', delete_company),

    path('company/',CompanyAPI.as_view()),
    # path('api/register/',UserAPI.as_view()),
    # path('get_employee/', get_employee),
    # path('post_employee/', post_employee),

    ################################## USER PATHS ################################
    path('home/', home, name='home'),
    path('register/', register, name="register"),
    path('login/', loginuser, name="login"),
    path('logout/', logoutuser, name='logout')
]
