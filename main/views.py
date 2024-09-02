from django.shortcuts import render, HttpResponse, redirect
from PIL import Image
from django.db.models.functions import Random
from django.core.files.uploadedfile import UploadedFile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Post
@login_required(login_url="login")
def home(request):
    # Retrieve the user profile
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect("/update")
    posts = Post.objects.order_by(Random())
    context = {'user_profile': user_profile, 'posts': posts}
    return render(request, 'home.html', context)
def signup(request):
    return render(request,'signup.html')
def loginpage(request):
    if request.user.is_authenticated:
         return redirect('home')
    else:
        return render(request, "login.html")

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect("signup")
        if not username.isalnum():
            messages.error(
                request, "Username should contain both/only letters and numbers.")
            return redirect("signup")
        users = User.objects.filter(username=username)
        if users.exists():
            messages.error(request, "The username is already in use.")
            return redirect('signup')
        if len(password) < 8:
            messages.error(request, "Password must be of eight characters!")
            return redirect('signup')
        if not password.isalnum():
            messages.error(
                request, "Your password must contain a alphabet and number!")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request,"This email is already in use! Try to login?")
            return redirect('signup')
        
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(
            request, "Your CommuniNepal account has successfully been created!")
        return redirect('update')
    else:
        return HttpResponse("404 - Not found")


def handleLogin(request):
    if request.method=="POST":
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username=loginusername, password= loginpassword)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect('login')

    return HttpResponse("404- Not found")      


@login_required(login_url="login")
def handleLogout(request):
        logout(request)
        messages.success(request,"Successfully Logged Out!")
        return redirect('/login')


@login_required(login_url="login")
def update(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = Profile(user=request.user)
        user_profile.save()
        
    if request.method == 'POST':
        image = request.FILES.get('profile_picture')
        bio = request.POST["bio"]
        location = request.POST["location"]
        
        if image is not None:
            if bio:
                user_profile.bio = bio
            if location:
                user_profile.location = location
            user_profile.profile_picture = image
            user_profile.save()
            
            # Update the profile picture in the posts
            Post.objects.filter(user=request.user).update(pp=image)
            
            messages.success(request, "Your profile was successfully edited!")
        
        return redirect('home')
    return render(request, "update.html", {"user_profile": user_profile})

@login_required(login_url="login")
def createpost(request):
    if request.method == "POST":
        user_profile = Profile.objects.get(user=request.user)
        picture = request.FILES.get('post_image')
        content = request.POST.get("post_content")
        
        user_post = Post.objects.create(
            user=request.user,
            pp=user_profile.profile_picture,
            post_picture=picture,
            content=content
        )
        
        user_post.save()
        messages.success(request, "Your post has been successfully created!")
        return redirect('/')
    
    return render(request, "createpost.html")