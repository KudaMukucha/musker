from django.shortcuts import get_object_or_404, redirect, render
from .models import Profile,Meep
from django.contrib import messages
from . forms import MeepForm, SignUpForm,ProfilePicForm
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from django import forms

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request,'Your meep has been posted...')
                return redirect('home')
        meeps = Meep.objects.all().order_by('-created_at')
        return render(request,'home.html',{'meeps':meeps,'form':form})
    else:
         meeps = Meep.objects.all().order_by('-created_at')
         return render(request,'home.html',{'meeps':meeps})
    
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request,'profile-list.html',{'profiles':profiles})
    else:
        messages.success(request,'You must be logged in to view this page..')
        return redirect('home')
    
def profile(request,pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(id = pk)
        meeps = Meep.objects.filter(user_id = pk).order_by('-created_at')
        #post follow unfollow logic
        if request.method == 'POST':
            #get current_user id
            current_user_profile = request.user.profile
            #get form data
            action = request.POST['follow']
            #decide to follow or unfollow
            if action == 'unfollow':
                current_user_profile.follow.remove(profile)
            elif action == 'follow':
                current_user_profile.follow.add(profile)
            #save the profile
            current_user_profile.save()
        return render(request,'profile.html',{'profile':profile,'meeps':meeps})
    else:
        messages.success(request,'You must be logged in to view this page')
        return redirect('home')
    
def login_user(request):
    if request.method  == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'You have been logged in...')
            return redirect('home')
        else:
            messages.success(request,'There was an error logging in, try again')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out. Thanks for spending some quality time with the musker site today.')
    return redirect('login')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            #Login user
            user = authenticate(request,username=username,password=password)
            login(request,user)
            messages.success(request,'You have successfully registered...')
            return redirect('home')
    return render(request,'register.html',{'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        profile_user = Profile.objects.get(user__id = request.user.id)
        #get forms
        user_form = SignUpForm(request.POST or None,request.FILES or None,instance = current_user)
        profile_form = ProfilePicForm(request.POST or None,request.FILES or None,instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile have been updated')
            return redirect('home') 
        return render(request,'update-user.html',{'user_form':user_form,'profile_form':profile_form})
    else:
        messages.error(request,'You must be logged in to view that page')
        return redirect('home')
    
def meep_like(request,pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep,id=pk)
        if meep.likes.filter(id= request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'You must be logged in to like meeps...')
        return redirect('home')
    
def meep_show(request,pk):
    meep = get_object_or_404(Meep,id=pk)
    if meep:
        return render(request,'meep.html',{'meep':meep})
    else:
        messages.success(request,'That meep does not exist...')
        return redirect('home')
    
def unfollow(request,pk):
    if request.user.is_authenticated:
        #get profile to unfollow
        profile = Profile.objects.get(user__id = pk)
        #unfollow user
        request.user.profile.follow.remove(profile)
        #save profile
        request.user.profile.save()
        #return message
        messages.success(request,(f"You have unfollowed {profile.user.username}"))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request,'You must be logged in to view this page...')
        return redirect('home')

def follow(request,pk):
    if request.user.is_authenticated:
        #get profile to unfollow
        profile = Profile.objects.get(user__id = pk)
        #unfollow user
        request.user.profile.follow.add(profile)
        #save profile
        request.user.profile.save()
        #return message
        messages.success(request,(f"You have followed {profile.user.username}"))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request,'You must be logged in to view this page...')
        return redirect('home')
    

def followers(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user__id = pk)
            return render(request,'followers.html',{'profiles':profiles})
        else:
            messages.success(request,'That is not your profile page...')
            return redirect('home')
    else:
        messages.success(request,'You must be logged in to view this page..')
        return redirect('home')

def follows(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user__id = pk)
            return render(request,'follows.html',{'profiles':profiles})
        else:
            messages.success(request,'That is not your profile page...')
            return redirect('home')
    else:
        messages.success(request,'You must be logged in to view this page..')
        return redirect('home')
    

def delete_meep(request,pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep,id=pk)
        #check to see you own the meep
        if request.user.username == meep.user.username:
            #delete the map
            meep.delete()
            messages.success(request,'The meep has been deleted...')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request,'You do not own that meep...')
            return redirect('home')
    else:
        messages.success(request,'Please login to delete...')
        return redirect(request.META.get('HTTP_REFERER'))
    
def edit_meep(request,pk):
    if request.user.is_authenticated:
        #grab the meep
        meep = get_object_or_404(Meep,id=pk)
        #check to see you own the meep
        if request.user.username == meep.user.username:
            form = MeepForm(request.POST or None,instance=meep)
            if request.method == 'POST':
                if form.is_valid():
                    meep = form.save(commit=False)
                    meep.user = request.user
                    meep.save()
                    messages.success(request,'Your meep has been updated...')
                    return redirect('home')
            else:
                return render(request,'edit-meep.html',{'form':form,'meep':meep})
        else:
            messages.success(request,'You do not own that meep...')
            return redirect('home')
    else:
        messages.success(request,'Please login to edit...')
        return redirect('home')
    
def search(request):
    if request.method == 'POST':
        #grab form input
        search = request.POST['search']
        #search the database
        searched =  Meep.objects.filter(body__contains == search)
        return render(request,'search.html',{'search':search,'searched':searched})
    else:
        return render(request,'search.html')
    
def search_user(request):
    if request.method == 'POST':
        #grab form input
        search = request.POST['search']
        #search the database
        searched =  User.objects.filter(username__contains == search)
        return render(request,'search-user.html',{'search':search,'searched':searched})
    else:
        return render(request,'search-user.html')