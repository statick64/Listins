from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import LandlordPasswordChangeView
from .views_messaging import messaging_hub, send_message, get_unread_messages_count, start_conversation

app_name = 'housing'

urlpatterns = [
    path('', views.home, name='index'),
    path('landlord_home', views.landlord_home, name='landlord_home'),
    path('Contact', views.contact, name='contact'),
    path('add_property', views.add_property, name='add_property'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout_view , name='logout'),
    path('studentDetials', views.studentDetails, name='studentDetials'),
    path('studentProperties', views.studentProperties, name='studentProperties'),
    path('landlordProperty', views.landlord_properties, name='landlord_properties'),
    path('profile/', views.profile, name='landlord_profile'),
    path('landlord/subscription/', views.subscription_page, name='subscription_page'),
    path('landlord/subscribe/<str:plan>/', views.start_subscription, name='start_subscription'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('payment/error/', views.payment_error, name='payment_error'),
    path('password_change/', LandlordPasswordChangeView.as_view(), name='password_change'),
    path('property/<int:property_id>/view/', views.view_property, name='view_property'),
    path('property/<int:property_id>/book/', views.book_property, name='book_property'),
    path('property/<int:property_id>/edit/', views.edit_property, name='edit_property'),
    path('property/<int:property_id>/verify/', views.property_verification_upload, name='property_verification_upload'),
    path('property/image/<int:image_id>/delete/', views.delete_image, name='delete_image'),
    path('property/<int:property_id>/delete_main_image/', views.delete_main_image, name='delete_main_image'),
    
    # Messaging URLs
    path('messages/', messaging_hub, name='messaging_hub'),
    path('messages/send/', send_message, name='send_message'),
    path('messages/unread/', get_unread_messages_count, name='get_unread_messages_count'),
    path('messages/start/<int:property_id>/', start_conversation, name='start_conversation'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)