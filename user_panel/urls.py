from django.urls import path
from . import views

urlpatterns = [
    # path('user-panel/', views.UserPanelAdminView.as_view(), name='user_panel'),
    path('user-panel/', views.user_panel_view, name='user_panel'),
    path('user-account-edit/', views.user_account_edit, name='user_account_edit'),
    path('remove-user-avatar/', views.user_remove_avatar, name='remove_user_avatar'),
    path('profile-user-edit/', views.personal_user_edit, name='profile_user_edit'),
    path('change-password-user-panel/', views.change_password_user_panel, name='change_password_user_panel'),
    path('remove-account/', views.remove_account, name='remove_account'),

]
