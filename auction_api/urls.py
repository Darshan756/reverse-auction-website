from django.urls import path,include


urlpatterns = [
    path('users_api/', include('user_accounts.urls')),
   
]
