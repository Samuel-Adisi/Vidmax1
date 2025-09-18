from django.shortcuts import render
from.models import Video,YoutubeComment,Porfile,Videos
from.forms import Register
from django.shortcuts import redirect 
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from.forms import CreateForm
from.serializers import CreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import  JsonResponse
from django.http import HttpResponse
import json
from django.contrib.auth.models import User

import cv2
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import redirect, render
from .forms import CreateForm

def get_video_duration(path):
    """
    Returns duration in seconds using OpenCV.
    """
    try:
        video = cv2.VideoCapture(path)
        if not video.isOpened():
            return 0
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        video.release()
        if fps == 0:  # avoid division by zero
            return 0
        return frame_count / fps
    except Exception as e:
        print(f"Error reading video duration: {e}")
        return 0

class Create(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        form = CreateForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()  # Save first to get file path

            if instance.video_file:
                duration_seconds = get_video_duration(instance.video_file.path)
                hours, remainder = divmod(int(duration_seconds), 3600)
                minutes, seconds = divmod(remainder, 60)

                if hours:
                    instance.duration = f"{hours}:{minutes:02}:{seconds:02}"
                else:
                    instance.duration = f"{minutes}:{seconds:02}"

                instance.save(update_fields=['duration'])

            return redirect('home')
        else:
            return redirect('create')

    def get(self, request):
        form = CreateForm()
        return render(request, 'create.html', {'form': form})


class Home(APIView):
  def get(self,request):
    media=Videos.objects.all()


    context={
        'videos':media,
    }
    return render(request,'index.html',context)
  

from django.http import JsonResponse


class uploadVideo(APIView):
  def get(self,request):
    videos = Videos.objects.all()
    video_list = []

    for video in videos:
        video_list.append({
            'id': video.id,
            'title': video.title,
            'author': video.author,
            'thumbnail_image': video.thumbnail_image.url if video.thumbnail_image else None,
            'video_file': video.video_file.url if video.video_file else None,
            'duration': video.duration,
            'published_at': video.published_at,  # DjangoJSONEncoder will handle datetime
        })
    return JsonResponse({'videos': video_list}, safe=False)


import requests
from django.shortcuts import render, get_object_or_404
from .models import Video, Videos, YoutubeComment,UploadComment

def video_view(request, videoId):
    video = None
    uploadVideo = None
    video_type = None

    try:
        # Try fetching uploaded video first
         uploadVideo = Videos.objects.get(video_id=videoId)
         video_type = "upload"
    except Videos.DoesNotExist:
        # If not found, fallback to YouTube
        video, created = Video.objects.get_or_create(video_id=videoId)
        video_type = "youtube"

        if created:  # fetch metadata only first time
            url = "https://www.googleapis.com/youtube/v3/videos"
            params = {
                "part": "snippet",
                "id": videoId,
                "key": "AIzaSyCz-So3EsZGHWV9nTYeRxZqSGKvdNxkn_M"
            }
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                if data["items"]:
                    snippet = data["items"][0]["snippet"]
                    video.title = snippet["title"]
                    video.author = snippet["channelTitle"]
                    video.thumbnail_url = snippet["thumbnails"]["high"]["url"]
                    video.published_at = snippet["publishedAt"]
                    video.save()

    if video_type == "youtube":
        comments = YoutubeComment.objects.filter(video=video).order_by('-created_at')
    else:
        comments = UploadComment.objects.filter(video=uploadVideo.id).order_by('-created_at')


    return render(
        request,
        "video_play.html",
        {
            "video": video,
            "uploadVideo": uploadVideo,
            "video_type": video_type,
            "comments": comments,
        },
    )



 

def signup(request):
    if request.method=='POST':
        form = Register(request.POST)
        username1=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
          if User.objects.filter(username=username1).exists():
              messages.info(request, 'Username already exists')
              return redirect('signup') 
          elif password1!=password2:
               messages.info(request, 'Passwords do not match')
          return redirect('signup') 
    else:
      form=Register()
      return render(request,'signup.html',{'form':form})
    
def signin(request):
    if request.method =='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Credentials not valid, check username or password')
            return redirect('signin')
    else:
        form=AuthenticationForm(None)
        return render(request,'login.html',{'form':form})

def signout(request):
    logout(request)
    return redirect('signin')


def search(request):
       data=request.POST.get('q')
       if data:
           suggestions=[]
           query=Video.objects.filter(title__icontains=data)[:10]
           suggestions=list(query.values('video_id','title'))

           if suggestions.__len__()>0 and len(data)>0:
              return JsonResponse({
                  'suggestions':suggestions
                 })
           else:
             return JsonResponse({
                  'suggestions':'no result found'
                 })
           
def result(request,pk):
    video=Video.objects.get(id=pk)

    return render(request,'result.html',{'video':video})

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Video, Videos, YoutubeComment, UploadComment

def comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login first to add comments'}, status=401)

    if request.method == 'POST':
        comment_text = request.POST.get('comment', '').strip()
        video_id = request.POST.get('video_id')
        video_type = request.POST.get('video_type') 

        if not comment_text:
            return JsonResponse({'error': 'Comment cannot be empty'}, status=400)

        if video_type == "youtube":
            # YouTube comment
            video = get_object_or_404(Video, video_id=video_id)
            YoutubeComment.objects.create(
                user=request.user,
                video=video,
                comment=comment_text
            )

        elif video_type == "upload":
            # Uploaded video comment
            video = get_object_or_404(Videos, id=video_id)
            UploadComment.objects.create(
                user=request.user,
                video=video,
                comment=comment_text
            )
        else:
            return JsonResponse({'error': 'Invalid video type'}, status=400)

        return JsonResponse({'msg': 'Comment submitted successfully'}, status=201)

    return HttpResponse('Invalid request', status=405)



def user(request):
   return HttpResponse('user dashboard')
   

def shorts(request):
    return render(request,'shorts.html')
       
    
    
    
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
import os
from .models import Videos   

def download(request, video_id):
    video = get_object_or_404(Videos, id=video_id)

    file_path = video.video_file.path  

    if os.path.exists(file_path):
        video.download='True'
        video.save()
        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(file_path)
        )

    else:
        return HttpResponse("Video not found", status=404)



def downloaded(request):
    videos=Videos.objects.filter(download=True)
    return render(request, 'downloaded.html', {'videos':videos})

def deleteVideo(request):
    video_id=request.POST['video_id']
    video=Videos.objects.get(id=video_id)
    video.download=False
    video.save()
    return JsonResponse({'msg':'success'}, status=200)



