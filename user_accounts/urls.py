from django.urls import path
from .views import ListCreatUsers,ListUpdateUser

urlpatterns = [
    path('',ListCreatUsers.as_view(),name="buyer_list_creation"),
    path('user/<uuid:pk>',ListUpdateUser.as_view())
    
  
    
]
