from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from .views import UserRegistrationView
from .views import CustomDataView
from .views import UpdateLevelView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("", views.getRoutes),
    path('notes/', views.getNotes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register', UserRegistrationView.as_view(), name="register"),
    path('custom-data/', CustomDataView.as_view(), name='custom_data'),
    path('updateLevel/', UpdateLevelView.as_view(), name="update-level"),
]
