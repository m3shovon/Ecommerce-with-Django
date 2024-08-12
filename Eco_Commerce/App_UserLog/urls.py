from django.urls import path
from App_UserLog import views

app_name = 'App_UserLog'

urlpatterns = [
    path('log/', views.user_log, name='userlog'),
    # path('user-logs/', views.UserLogList.as_view(), name='user-log-list'),
    # path('user-logs/<int:pk>/', views.UserLogDetail.as_view(), name='user-log-detail'),
]