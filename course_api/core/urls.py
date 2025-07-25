from django.urls import path
from . import views

urlpatterns = [
    path('basic_info', views.basic_info),
    path('course_outcome', views.course_outcome),
    path('syllabus', views.syllabus),
    path('questions', views.questions),
    path('course_materials', views.course_materials),
    path('process_file', views.process_file),
    path('user_request', views.user_request),
]
