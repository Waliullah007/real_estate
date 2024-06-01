from django.urls import path
from . import views

urlpatterns= [
    path('',views.listings,name='listings'),

    path('<str:listing_id>/',views.listing,name='listing'),

    path('search',views.search,name='search'),
]    