from django.urls import path
from .views import getUsers,registerUser,loginUser,updateUser

urlpatterns = [
    path('<str:pk>', getUsers),
    path('register/',registerUser),
    path('login/',loginUser),
    path('update/',updateUser),
]