from django.urls import path
from .views import *

urlpatterns = [
    path('pdf', Pdf.as_view())
]
