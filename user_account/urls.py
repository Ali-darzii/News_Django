from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.SignUpView.as_view(), name='sign_up'),
    path('sign-in', views.SignInView.as_view(), name='sign_in'),
    path('sign-out', views.SignOut.as_view(), name='sign_out'),
    path('forget-password', views.ForgetPasswordView.as_view(), name='forget_password_page'),
    path('activate-account/<email_active_code>', views.ActivateAccountView.as_view(), name='activate_account')
]
