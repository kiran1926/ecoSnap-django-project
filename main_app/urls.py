from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('map/', views.sighting_map_view, name='map_view'), 
    path('sighting/<int:sighting_id>/', views.sighting_detail_view, name='sighting_detail'),
    path('sighting/create/', views.sighting_create_view, name='sighting_create'),
    path('sighting/<int:sighting_id>/edit/', views.sighting_update_view, name='sighting_edit'),
    path('sighting/<int:sighting_id>/delete/', views.sighting_delete_view, name='sighting_delete'),
    path('api/analyze-image/', views.analyze_image, name='analyze_image'),
 
] 