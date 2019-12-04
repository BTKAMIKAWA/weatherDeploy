from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^search_address$', views.address),
    url(r'^search_db$', views.searchdb),
    url(r'^filter_city', views.city)
]