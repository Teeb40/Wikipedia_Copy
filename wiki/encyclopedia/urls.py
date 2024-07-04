from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entry", views.entry, name="entry"),
    path("<str:title>",views.title_,name="title"),
    path("edit/<str:edit_page>",views.edit,name="edit")
    
    
]
