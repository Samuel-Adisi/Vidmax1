from django.urls import path
from. import views 

urlpatterns=[
    path('home/',views.Home.as_view(),name='home'),
    path('',views.Home.as_view(),name='home'),
    path('video_view/<str:videoId>/',views.video_view,name='video_view'),
    path('signup/',views.signup,name='signup'),
    path('signout/',views.signout,name='signout'),
    path('signin/',views.signin,name='signin'),
    path('create/',views.Create.as_view(),name='create'),
    path('search/',views.search,name='search'),
    path('result/<int:pk>/',views.result,name='result'),
    path('comment/',views.comment,name='comment'),
    path('user/',views.user,name='user'),
    path('shorts/',views.shorts,name='shorts'),
    path('videos/',views.uploadVideo.as_view(), name='videos'),
    path('download/<int:video_id>/', views.download, name='download'),
    path('downloaded/', views.downloaded, name='downloaded'),
    path('delete/', views.deleteVideo, name='delete'),
 
]