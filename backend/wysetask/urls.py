from django.urls import path
from .views import getUsers,registerUser,loginUser,updateUser

urlpatterns = [
    path('profile/view/<str:pk>', getUsers),
    path('register/',registerUser),
    path('login/',loginUser),
    path('profile/edit/',updateUser),
]