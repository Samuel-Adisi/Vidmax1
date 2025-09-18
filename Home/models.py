from django.db import models
from django.contrib.auth.models import User


# Create your models here.

from django.db import models

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    video_id = models.CharField(max_length=50, unique=True)  # YouTube video ID
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)  # channel name
    thumbnail_url = models.URLField()  # YouTube thumbnail link
    published_at = models.DateTimeField(auto_now_add=True, null=True)  # published date from YouTube
    duration = models.CharField(max_length=20, blank=True, null=True)  # optional

    def __str__(self):
        return self.title


class Videos(models.Model):
    id = models.AutoField(primary_key=True)
    video_id=models.CharField(max_length=50, unique=True,default='')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)  # channel name
    thumbnail_image = models.FileField(upload_to='media/thumbnail/')  # YouTube thumbnail link
    video_file = models.FileField(upload_to='media/video/')  # local video file
    published_at = models.DateTimeField(auto_now_add=True, null=True)  # published date from YouTube
    duration = models.CharField(max_length=20, blank=True, null=True)  # optional
    download=models.BooleanField(default=False)

    def __str__(self):
        return self.title

   


class YoutubeComment(models.Model):
    video=models.ForeignKey(Video,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,default="")
    comment=models.CharField(default="", max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)



    def __str__(self):
        return self.user.username
    

class UploadComment(models.Model):
    video=models.ForeignKey(Videos,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,default="")
    comment=models.CharField(default="", max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)



    def __str__(self):
        return self.user.username
    
class Porfile(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True,default="")
    image=models.ImageField(upload_to='thumbnail/')
        


    




    


    



