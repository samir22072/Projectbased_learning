
from django.contrib.auth.models import User, UserManager
from django.db import models
from django.conf import settings
import os 
import random
from django.contrib.auth.models import User
import hashlib
from threading import Timer



def file_path_encoder(instance,filename):
        """This function is used to provide a hashed,unique and secure imagepath 
        to the media folder.It also tunnels intermediate values for exporting using tunnel function.
        The output format is {unique-52-char-code}.{basefile-extension} """

        y= hashlib.sha256(("".join(map(str,[random.randint(0,9) for i in range(10)]))).encode('utf-8')).hexdigest()[0:52]
 
        instance.original_file_name = filename
        base,ext = filename.split(".")
  
        new_name = f"{str(y)}.{ext}"
        tunnel(new_name)
        from .views import show_shoulder_width
        Timer(1, show_shoulder_width).start()
        return os.path.join(r'C:\Users\samir\pbl\media\images',new_name)


 
class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg', upload_to='profile_pics')
    scan_image = models.ImageField(upload_to = file_path_encoder,null=True,blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'



def tunnel(path):
        """Function to smuggle values over the 7 seas of django (stupidity) """
        global x 
        x = path



