from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'housing'

urlpatterns = [
    path('', views.home, name='index'),
    path('landlord_home', views.landlord_home, name='landlord_home'),
    path('add_property', views.add_property, name='add_property'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout_view , name='logout'),
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)