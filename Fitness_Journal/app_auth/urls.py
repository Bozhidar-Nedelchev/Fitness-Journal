from django.urls import path
from Fitness_Journal.app_auth.views import RegisterUserView, LoginUserView, LogoutUserView
urlpatterns = (
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout/', LogoutUserView.as_view(),name='logout_user'),

)