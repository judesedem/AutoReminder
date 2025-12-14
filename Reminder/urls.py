from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView,ReminderListCreateView,ReminderDetailView,CustomLogin
 

urlpatterns=[
    #Auth endpoints
    path('register/',RegisterView.as_view(), name='register'),    
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh',TokenRefreshView.as_view(),name='token_refresh'),
    path('login/',CustomLogin.as_view()),
  
    #Reminder endpoints
    path('reminders/',ReminderListCreateView.as_view(),name='reminder-list'),
    path('reminders/<int:pk>/',ReminderDetailView.as_view(),name='reminder-detail')    
     
]