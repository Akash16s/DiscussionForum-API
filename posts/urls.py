from django.urls import path, include
from .views import *

urlpatterns = [
    path('list/', postHandler.as_view(), name="Handle posts"),
    path('list/<id>/', postHandler.as_view(), name="Handle posts"),
    path('comment/', commentView.as_view(), name="Handle Comment"),
    path('comment/<id>/', commentView.as_view(), name="Handle Comment"),
    path('tag/', tagView.as_view(), name="Handle tags"),
    path('tag/<id>/', tagView.as_view(), name="Handle tags"),
]
