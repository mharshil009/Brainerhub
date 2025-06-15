from django.urls import path
from .views import UploadEmployeeData

urlpatterns = [
    path('v1/upload/', UploadEmployeeData.as_view(), name='upload-data'),
]
