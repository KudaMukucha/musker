from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

#Create meep model
class Meep(models.Model):
    user = models.ForeignKey(User,related_name='meeps',on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='mee_like', blank=True)

    #keep track of likes
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return( f'{self.user}'
                f'({self.created_at:%Y-%m-%d %H:%M}):'
                f'{self.body}...'
                )
               
#create user profile
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    follow = models.ManyToManyField("self",related_name='followed_by',symmetrical=False,blank=True)
    date_modified = models.DateTimeField(User,auto_now=True)
    profile_image = models.ImageField(null=True,blank=True,upload_to="images/")
    profile_bio =  models.CharField(null=True,blank=True,max_length=140)
    homepage_link = models.CharField(null=True,blank=True,max_length=140)
    facebook_link = models.CharField(null=True,blank=True,max_length=140)
    instagram_link = models.CharField(null=True,blank=True,max_length=140)

    def __str__(self):
        return self.user.username


#Create new profile when new user signs up
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()
        #user follows himself
        user_profile.follow.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)

