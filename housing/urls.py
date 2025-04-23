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
    path('studentDetials', views.studentDetails, name='studentDetials'),
    path('studentProperties', views.studentProperties, name='studentProperties'),
    # path('editProperty', views.editProperty, name='editProperty'),
    path('property/<int:property_id>/view/', views.view_property, name='view_property'),
    path('property/<int:property_id>/edit/', views.edit_property, name='edit_property'),
    path('property/image/<int:image_id>/delete/', views.delete_image, name='delete_image'),
    
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)