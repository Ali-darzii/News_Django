from django.urls import path
from . import views

urlpatterns = [
    path('user-panel', views.UserPanelAdminView.as_view(), name='user_panel')
]
