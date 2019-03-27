from django.urls import re_path
from . import views
from django.contrib.auth.views import (
        PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, LoginView
        )
from django.contrib.auth.models import User
app_name = 'accounts'




urlpatterns = [
        re_path(r'^$', views.home, name="home"),
        re_path(r'^login/$', views.login_view, name="login"),
        re_path(r'^logout/$', views.logout_view, name="logout"),
        re_path(r'^signup/$', views.signup_view, name="signup"),
        re_path(r'^setting/(?P<username>\w+)/$', views.settings_view, name="settings"),
        re_path(r'^delete_confirm/$', views.delete_view, name="delete"),
        re_path(r'^delete/$', views.delete_account, name="delete_account"),
        re_path(r'^signup/details/$', views.signup_detailsview, name="details"),
        re_path(r'^profile/(?P<username>\w+)/$', views.view_profile, name="profile"),
        #re_path(r'^profile/(?P<username>\w+)/$', views.view_other, name="others_profile"),
        re_path(r'^profile/edit/(?P<username>\w+)/$', views.edit_profile, name="edit_profile"),
        re_path(r'^change-password/$', views.change_password, name="change_password"),
        re_path(r'^reset-password/$', PasswordResetView.as_view(template_name='accounts/reset_password.html', email_template_name="accounts/reset_password_email.html", success_url="done/"), name="password_reset"),
        re_path(r'^reset-password/done/$', PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html'), name="password_reset_done"),
        re_path(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(template_name="accounts/reset_password_confirm.html"), name="password_reset_confirm"),
        #path('reset/done', PasswordResetCompleteView.as_view(template_name="accounts/reset_password_complete.html"), name="password_reset_complete"),
        re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]
