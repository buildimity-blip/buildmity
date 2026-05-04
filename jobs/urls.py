from django.urls import path
from .views import create_job, my_jobs, available_jobs, assign_job, assigned_jobs

urlpatterns = [
    path('create/', create_job, name='create_job'),
    path('my/', my_jobs, name='my_jobs'),
    path('available/', available_jobs, name='available_jobs'),
    path('assign/<int:job_id>/', assign_job, name='assign_job'),
    path('assigned/', assigned_jobs, name='assigned_jobs'),
]