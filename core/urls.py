from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path ('', views.ReviewListView.as_view(), name='inicio'),
    path ('info', views.info, name='info'),
    path ('ventajas', views.ventajas, name='ventajas'),
    path ('martillos', views.HammerListView.as_view(), name='martillos'),
    path ('review/create/', ReviewCreate.as_view(), name="review_create"),
    path ('hammer/<int:id>', HammerDetailView.as_view(), name="hammer_detail"),
    path ('review/<int:id>', ReviewDetailView.as_view(), name="review_detail"),
    path ('review/<int:id>/update/', ReviewUpdate.as_view(), name="review_update"),
    path ('review/<int:id>/delete/', ReviewDeleteView.as_view(), name="review_delete"),
    path ('hammer/search/', HammerListView.as_view(), name="hammer_search"),
    path ('login/', UserLoginView.as_view(), name='login'),
    path ('register/', UserRegisterView.as_view(), name='register' ),
    path ('logout/', UserLogoutView.as_view(), name='logout')
]
