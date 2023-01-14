from django.urls import path

from . import views

app_name = "cucumber_leaf_face"

urlpatterns = [
    path("showall/", views.showall, name="showall"),
    path("upload/", views.upload, name="upload"),
    path("result/", views.result, name="result"),
]

