from django.urls import path, include
from app import views

app_name = "app"

urlpatterns = [
    path('', views.index, name='index'),
    path('detect', views.face_detact, name='face-detect'),
    path('facecam_feed', views.facecam_feed, name='facecam_feed'),
    ]