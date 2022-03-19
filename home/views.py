from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import os.path
from home.models import User
import os
from django.conf import settings


PROFILE_PIC_FOLDER='static/images/profile-pics/' 
def index(request):
    context = {"username":request.session.get('username')}
    return render(request, 'home/index.html',context)

def signup(request):
    if request.method =='POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        type = 'user'
        profile_pic = request.FILES.get('profile_pic')
        extension = os.path.splitext(profile_pic.name)[1][1:]
        new_name = username +'.'+ extension
        fs = FileSystemStorage(location=PROFILE_PIC_FOLDER) #defaults to   MEDIA_ROOT  
        filename = fs.save(new_name, profile_pic)
        file_url = fs.url(filename)

        Users = User(username=username, email=email, password=password,profile_pic=new_name,type=type)
        Users.save()
        print("user added to database")
        context= {'signup': "success","username":request.session.get('username')}
        return render(request, 'home/index.html',context)

def login(request):
    try:
        if request.method =='POST':
            username = request.POST.get("username")
            password = request.POST.get("password") 
            userName = None   
            try:
                userName = User._meta.get_field('password').value_from_object(User.objects.get(username=username))
                userid = User._meta.get_field('id').value_from_object(User.objects.get(username=username))
                type = User._meta.get_field('type').value_from_object(User.objects.get(username=username))
                print("userid: ",userid)
            except Exception as e:
                print(e)
            if userName is not None:
                if password == userName:
                    request.session['username'] = username
                    request.session['userid'] = userid
                    request.session['type'] = type
                    request.session['is_login'] = True
                    context= {"username":request.session.get('username')}
                    return render(request, 'home/index.html',context)
                else:
                    context= {'error': "true","msg":"Incorrect Password"}
                    return render(request, 'home/index.html',context)
            else:
                context= {'error': "true","msg":"Username doesn't exist"}
                return render(request, 'home/index.html',context)
    except Exception as e:
        return HttpResponse(e)

def logout(request):
    try:
        del request.session['username'] 
        del request.session['userid']
        request.session['is_login'] = False
        context= {"username":request.session.get('username')}
        return render(request, 'home/index.html',context)
    except Exception as e:
        return HttpResponse(e)
            
    

def admin_dashboard(request):
    if request.session['is_login'] is True:
        if request.session['type'] == 'admin':
            admin_data = User.objects.all().filter(id=request.session.get('userid'))
            context = {"user_data":admin_data}
            return render(request,'home/admin-dashboard.html',context)
        else:
            return render(request,"home/admin-login.html")
    else:
        return render(request,"home/admin-login.html")
    

def admin_login(request):
    try:
        if request.method =='POST':
            username = request.POST.get("username")
            password = request.POST.get("password") 
            userName = None   
            try:
                userName = User._meta.get_field('password').value_from_object(User.objects.get(username=username))
                userid = User._meta.get_field('id').value_from_object(User.objects.get(username=username))
                type = User._meta.get_field('type').value_from_object(User.objects.get(username=username))
                print("userid: ",userid)
            except Exception as e:
                print(e)
            if userName is not None:
                if password == userName:
                    if type == 'admin':
                        request.session['username'] = username
                        request.session['userid'] = userid
                        request.session['type'] = type
                        request.session['is_login'] = True
                        context= {"username":request.session.get('username')}
                        return render(request, 'home/admin-dashboard.html',context)
                    else:
                        context= {'alert': "true","msg":"This user doesn't have admin rights"}
                        return render(request, 'home/admin-login.html',context)
                else:
                    context= {'alert': "true","msg":"Incorrect Password"}
                    return render(request, 'home/admin-login.html',context)
            else:
                context= {'alert': "true","msg":"Username doesn't exist"}
                return render(request, 'home/admin-login.html',context)
    except Exception as e:
        return HttpResponse(e)

def admin_users(request):
    if request.session['is_login'] is True:
        if request.session['type'] == 'admin':
            users_data = User.objects.all().filter(type="user")
            user_data = User.objects.all().filter(id=request.session.get('userid'))
            context = {'users_data':users_data,"user_data":user_data}
            return render(request,'home/admin-users.html',context)
        else:
            return HttpResponse("please log in first")
    else:
        return HttpResponse("please log in first")

def delete_user(request, id):
    
    if request.session['is_login'] is True:
        if request.session['type'] == 'admin':
            User.objects.filter(id=id).delete()
            user_data = User.objects.all().filter(type="user")
            context = {'user_data':user_data,"alert":"success","msg":"User Deleted"}
            return render(request,'home/admin-users.html',context)
        else:
            return HttpResponse("please log in first")
    else:
        return HttpResponse("please log in first")
    
def admin_profile(request):
    if request.session['is_login'] is True:
        if request.method =='POST':
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            profile_pict = request.FILES.get('profile_pic')
            type = 'admin'

            t = User.objects.get(id=request.session.get('userid')) 
            
            if profile_pict:
                old_profile_pic = t.profile_pic
                # now delete old profile pic 
                fs = FileSystemStorage(location=PROFILE_PIC_FOLDER) #defaults to   MEDIA_ROOT  
                filename = fs.delete(old_profile_pic)
                extension = os.path.splitext(profile_pict.name)[1][1:]
                new_name = username +'.'+ extension
                fs = FileSystemStorage(location=PROFILE_PIC_FOLDER) #defaults to   MEDIA_ROOT  
                filename = fs.save(new_name, profile_pict)
                t.profile_pic = new_name
            t.username = username
            t.email = email
            t.password = password
            t.save()
            user_data = User.objects.all().filter(id=request.session.get('userid'))
            context= {'alert': "success","msg":"Profile Updated!","user_data":user_data}
            return render(request, 'home/admin-profile.html',context)

        user_data = User.objects.all().filter(id=request.session.get('userid'),type='admin')
        context = {"user_data":user_data}
        return render(request,'home/admin-profile.html',context)
    else:
        return HttpResponse("please log in first")

