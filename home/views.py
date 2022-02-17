from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# HTML Pages
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)

        if len(name)<2 or len(email)<4 or len(phone)<10 or len(content)<4:
            messages.error(request, 'Please fill the form correctly.')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Form filled successfully.')
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none()

    #allPosts = Post.objects.all()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request, 'No result found')
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html',params)
    #return HttpResponse("search")

# Authentication APIS
def handleSignup(request):
    if request.method == 'POST':
        # Get the POST parameter
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        #Check for errorneous input
        if len(username) > 20:
            messages.error(request, 'Enter Valid Username.')
            return redirect('home')
        if not username.isalnum():
            messages.error(request, 'Username should only consist of alphabets and numbers.')
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, 'Password do not match.')
            return redirect('home')

        #Create User
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request, 'Your account has been created successfuly.')
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        # Get the POST parameter
        loginusername=request.POST['loginusername']
        loginpass1=request.POST['loginpass1']

        user = authenticate(username=loginusername, password=loginpass1)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Login")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')    

    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logout")
    return redirect('home') 

    return HttpResponse('handleLogout')
