from.models import UserComment,Video
class Comment():

     def __init__(self,request,video_id):
        print('video id is',video_id)
     
        self.session=request.session #this creates a session 
        

        cart=self.session.get('session_key')
        if 'session_key' not in request.session:
            cart=self.session['session_key']={}# this a session of empty list
        
        self.request=request
        self.cart=cart #allows you access the session globally
      
        carty=str(self.cart)    
        carty=carty.replace("\'","\"")
    
        if self.request.user.is_authenticated:
            #Get the current user          
            video=Video.objects.get(id=video_id)
            current_user=UserComment.objects.get(videos=video)
            current_user.comment=str(carty)
            current_user.save()
            
          

     def add(self,number,text,request):
        number=str(number)
        if number in self.session:
            number.replace(number,number)
        else:   
         self.cart[number]=(text)
         self.session.modified= True

     def retrive_comments(self):
          comments=UserComment.objects.filter(user=self.request.user)
          return comments