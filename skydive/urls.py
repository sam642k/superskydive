from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import ResetPasswordView

app_name = 'skydive'
urlpatterns = [
    path("", views.index, name="index"),
    path('skydive/login', views.login, name='login'),
    path('skydive/register', views.Register.as_view(), name='register'),
    path('skydive/logout', views.logout, name='logout'),
    path('skydive/reset', ResetPasswordView.as_view(), name='reset'),
    path('skydive/password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='skydive/password_reset_confirm.html',
                                                     success_url=reverse_lazy('skydive:password_reset_complete')),
         name='password_reset_confirm'),
    path('skydive/password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='skydive/password_reset_complete.html'),
         name='password_reset_complete'),
    path('skydive/search', views.search, name='search'),
    path('skydive/search/<str:destination>', views.search_loc, name='search_loc'),
    path('skydive/search/<str:skydive_type>/<int:desc_id>', views.type_skydive, name='type_skydive'),
    path('skydive/booking/<int:dest_id>/', views.booking, name='booking'),
    path('skydive/payment/<int:dest_id>', views.booking, name='payment'),
    path('skydive/card_payment/<int:booking_id>', views.card_payment, name='card_payment'),
    path('skydive/otp_verification', views.otp_verification, name='otp_verification'),
    path('skydive/mybookings', views.mybookings, name='mybookings'),
    path('skydive/cancelbooking', views.cancel_booking, name="cancelbooking"),
    path('skydive/about', views.about, name='about'),
    path('skydive/joinus', views.JoinUs.as_view(), name='joinus'),
    path('skydive/subscribe', views.subscribe, name='subscribe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
