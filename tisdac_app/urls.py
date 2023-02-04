from tisdac_app import views
from django.urls import path
from django.views.decorators.cache import cache_page
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', cache_page(0)(views.home), name='tisdac-main'),
    path('about', cache_page(0)(views.about), name='tisdac-about'),
    path('contact', views.ContactView.as_view(), name='tisdac-contact'),
    path('contact/done', views.contact_done, name='tisdac-contact-done'),
    path('upcoming_events', cache_page(0)(views.upcoming_events), name='tisdac-upcoming_events'),
    path('upcoming_events/done', views.show_one_event_done, name='event-detail-done'),
    path('upcoming_events/<slug:slug_event>', views.ShowOneEventView.as_view(), name='event-detail'),
    path('activities', cache_page(0)(views.activities), name='tisdac-activities'),
    path('activities/<slug:slug_department>', views.show_one_activity, name='activity-detail'),
    path('services', cache_page(0)(views.services), name='tisdac-services'),
    path('services/<slug:slug_service>', views.show_one_service, name='service-detail'),
    path('news', views.news, name='tisdac-news'),
    path('news/<int:article_id>', views.show_one_article, name='news-detail'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.RegisterUser.as_view(), name='register'),
    #password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),




]
