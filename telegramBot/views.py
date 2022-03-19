from email import message
from django.shortcuts import render, redirect
from httplib2 import Http
from home.models import User
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import os.path
from telegramBot.models import Telegram_Accounts
from telegramBot.models import Telegram_Groups
from telegramBot.models import Telegram_Questions
from telegramBot.models import Telegram_Answers
from telegramBot.models import Schedule_Messages
from django.conf import settings
import time
import asyncio
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import *
from telethon import functions
import sys
from datetime import datetime
import time
import os

PROFILE_PIC_FOLDER='static/images/profile-pics/' 
TELEGRAM_CHAT_FOLDER='static/images/chat-pics/' 
TELEGRAM_SESSIONS_FOLDER= settings.BASE_DIR
# Create your views here.


def user_dashboard(request):
    if request.session['is_login'] is True:
        user_data = User.objects.all().filter(id=request.session.get('userid'))
        Telegram_account_count = Telegram_Accounts.objects.filter(userid=request.session.get('userid')).count()
        questions_count = Telegram_Questions.objects.filter(userid=request.session.get('userid')).count()
        answers_count = Telegram_Answers.objects.filter(userid=request.session.get('userid')).count()
        messages_count = Schedule_Messages.objects.filter(userid = request.session.get('userid')).count()
        context = {"user_data":user_data,"telegram_account_count":Telegram_account_count,"questions_count":questions_count,"answers_count":answers_count,"messages_count":messages_count}
        return render(request,'telegramBot/user-dashboard.html',context)
    else:
        return HttpResponse("please log in first")

def user_profile(request):
    if request.session['is_login'] is True:
        if request.method =='POST':
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            profile_pict = request.FILES.get('profile_pic')

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
            context = {"user_data":user_data,'alert': "success","msg":"Profile Updated!"}
            return render(request, 'telegramBot/user-profile.html',context)

        user_data = User.objects.all().filter(id=request.session.get('userid'))
        context = {"user_data":user_data}
        return render(request,'telegramBot/user-profile.html',context)
    else:
        return HttpResponse("please log in first")


def telegram_dm_bot(request):
    if request.session['is_login'] is True:
        if request.method =='POST':
            hash_id = request.POST.get("hash_id")
            hash_key = request.POST.get("hash_key")
            number = request.POST.get("number")
            session_file = request.FILES.get("session_file")
            if session_file:
                filename = session_file.name
                filename = filename.replace("+","")
                fs = FileSystemStorage(location=TELEGRAM_SESSIONS_FOLDER) #defaults to   MEDIA_ROOT  
                filename = fs.save(filename,session_file)
                file_url = fs.url(filename)
                Account = Telegram_Accounts(userid=request.session.get('userid'), hash_id=hash_id, hash_key=hash_key,number=number,session_file=filename)
                Account.save()
            else:
                Account = Telegram_Accounts(userid=request.session.get('userid'), hash_id=hash_id, hash_key=hash_key,number=number)
                Account.save()
                
            return redirect("telegram_dm_bot")
        user_data = User.objects.all().filter(id=request.session.get('userid'))
        telegram_accounts = Telegram_Accounts.objects.all().filter(userid=request.session.get('userid'))
        context= {"username":request.session.get('username'),"user_data":user_data,"telegram_accounts":telegram_accounts}
        return render(request,'telegramBot/telegram-dm-bot.html',context)  
    else:
        return HttpResponse("please log in first")

def telegram_dmBot_send(request,id, sent):
    if request.session['is_login'] is True: 
        account = Telegram_Accounts.objects.all().filter(id=id)
        user_data = User.objects.all().filter(id=request.session.get('userid'))
        groups = Telegram_Groups.objects.all().filter(userid=request.session.get('userid'),account_id=id)
        questions = Telegram_Questions.objects.all().filter(userid=request.session.get('userid'),account_id=id)
        accounts = Telegram_Accounts.objects.all().filter(userid=request.session.get('userid'))
        context= {"username":request.session.get('username'),"user_data":user_data,"account":account,"groups":groups,"questions":questions,"sent":sent,"accounts":accounts}
        return render(request,"telegramBot/telegram-dmBot-send.html",context)
            
            
    else:
        return HttpResponse("please log in first")

def telegram_client(phone, api_id, api_hash):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # client = TelegramClient(phone, api_id, api_hash)
    client = TelegramClient(phone, api_id, api_hash, loop=loop)
    time.sleep(3)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))
    return client

def send_chat(request,id):
    if request.session['is_login'] is True:
        if request.method =='POST':
            print( "post request received")
            type = request.POST.get("type")
            if type == "image":
                # return HttpResponse("imageeeeeeeeeeeeee")
                picture = request.FILES.get('message')
                fs = FileSystemStorage(location=TELEGRAM_CHAT_FOLDER) #defaults to   MEDIA_ROOT  
                filename = fs.save(picture.name, picture)
                print(filename)
                print("picture saved")
            else:
                chat = request.POST.get("message")

            group_name = request.POST.get("group_name")
            account_id = int(request.POST.get("account_id"))
            sleep_time_first = request.POST.get("delay")
            datetime2 = str(request.POST.get("datetime"))
            date = datetime2.rpartition('T')[0]
            time = datetime2.rpartition('T')[2]
            print(date)
            print(time)
            if type == "image":
                data = Schedule_Messages(userid=request.session.get('userid'), message=filename, account_id=account_id, group=group_name, delay = sleep_time_first, date=date, time=time,status="pending",type=type)
            else:
                data = Schedule_Messages(userid=request.session.get('userid'), message=chat, account_id=account_id, group=group_name, delay = sleep_time_first, date=date, time=time,status="pending",type=type)

            data.save()
            return HttpResponse("Scheduled")
    else:
        return HttpResponse("please log in first")
def send_answer(request,id):
    if request.session['is_login'] is True:
        if request.method =='POST':
            group_name = request.POST.get("group_name")
            answer = request.POST.get("answer")
            account_id = id
            print(group_name, answer, account_id)
            TelegramAccount = Telegram_Accounts.objects.all().filter(id=account_id)
            phone = TelegramAccount[0].number
            api_id = TelegramAccount[0].hash_id
            api_hash = TelegramAccount[0].hash_key
            sleep_time = int(TelegramAccount[0].sleep_time)
            sleep_time_first = int(TelegramAccount[0].sleep_time_first)
            print(phone,api_hash,api_id)

            try:
                client = telegram_client(phone, api_id, api_hash)
                print('Account login successfully')
            except PhoneCodeInvalidError:
                sys.exit('You enter the wrong code.')

            # group_name = "bottestcomm"
            client(functions.channels.JoinChannelRequest(channel=group_name))
            print('Bot send message after '+str(sleep_time_first)+' seconds.')
            time.sleep(sleep_time_first)
            while True:
                try:
                    # question = "Lets Groot?"
                    client.send_message(group_name, str(answer))
                    print('Question send successfully. Bot sleep for '+str(sleep_time)+ ' seconds.')
                    # url = "/telegram-dmBot-send/"+str(id)+"/true"
                    # return HttpResponseRedirect(url)
                    # redirect         
                    client.disconnect()         
                    account = Telegram_Accounts.objects.all().filter(id=id)
                    user_data = User.objects.all().filter(id=request.session.get('userid'))
                    groups = Telegram_Groups.objects.all().filter(userid=request.session.get('userid'),account_id=id)
                    answer = Telegram_Answers.objects.all().filter(userid=request.session.get('userid'),account_id=id)
                    context= {"username":request.session.get('username'),"user_data":user_data,"account":account, "category":"answer","groups":groups,"answers":answer,"sent":"true","group_name":group_name}
                    return render(request,"telegramBot/telegram-bot-send.html",context)
                    column += 1
                    time.sleep(sleep_time)
                except IndexError:         
                    client.disconnect()
                    print("All questions completed in "+group_name+' group.\n')
                    print()
                    url = "/telegramBot/telegram-dmBot-send/"+id
                    return HttpResponseRedirect(url)
                except FloodError:         
                    client.disconnect()
                    print('Due to many messages in group bot stops (Flood error).')
                    sys.exit()
                    url = "/telegramBot/telegram-dmBot-send/"+id
                    return HttpResponseRedirect(url)
                except FloodWaitError:         
                    client.disconnect()
                    print('Due to many messages in group bot stops (Flood error).')
                    sys.exit()
                    url = "/telegramBot/telegram-dmBot-send/"+id
                    return HttpResponseRedirect(url)
                except Exception as e:         
                    client.disconnect()
                    print(e)
                    sys.exit()
                    url = "/telegramBot/telegram-dmBot-send/"+id
                    return HttpResponseRedirect(url)

                except Exception as e:         
                    client.disconnect()
                    print(e)
                    url = "/telegramBot/telegram-dmBot-send/"+id
                    return HttpResponseRedirect(url)

            else:
                return HttpResponse("please log in first")

def telegram_bot_add_group(request, category):
    if request.session['is_login'] is True:
        if request.method =='POST':
            group_name = request.POST.get("group_name")
            userid = request.session.get('userid')
            account_id =request.POST.get("account_id")

            data = Telegram_Groups(group_name=group_name, userid=userid, account_id=account_id)
            data.save()
            url = "/telegramBot/telegram-dmBot-send/"+account_id+"/1"
            return HttpResponseRedirect(url)        

    else:
        return HttpResponse("please log in first")

def telegram_bot_add_question(request):
    if request.session['is_login'] is True:
        if request.method =='POST':
            questions = request.POST.get("questions")
            account_id =request.POST.get("account_id")
            userid = request.session.get('userid')
            print("ques ",questions)

            data = Telegram_Questions(questions=questions, userid=userid, account_id=account_id)
            data.save()
            url = "/telegramBot/telegram-dmBot-send/"+account_id+"/1"
            return HttpResponseRedirect(url)   

    else:
        return HttpResponse("please log in first")
def telegram_bot_add_answer(request):
    if request.session['is_login'] is True:
        if request.method =='POST':
            answers = request.POST.get("answer")
            account_id =request.POST.get("account_id")
            userid = request.session.get('userid')
            print("ques ",answers)

            data = Telegram_Answers(answers=answers, userid=userid, account_id=account_id)
            data.save()
            url = "/telegramBot/telegram-bot-send/answer/"+account_id+"/1"
            return HttpResponseRedirect(url)   

    else:
        return HttpResponse("please log in first")

def delete_telegram_account(request,id):
    if request.session['is_login'] is True:
        filename = Telegram_Accounts._meta.get_field('session_file').value_from_object(Telegram_Accounts.objects.get(id=id))
        Telegram_Accounts.objects.filter(id=id).delete()
        Telegram_Groups.objects.filter(account_id=id).delete()
        Telegram_Questions.objects.filter(account_id=id).delete()
        Telegram_Answers.objects.filter(account_id=id).delete()
        # todo for telegram answers too 
        if filename:
            fs = FileSystemStorage(location=TELEGRAM_SESSIONS_FOLDER) #defaults to   MEDIA_ROOT  
            filename = fs.delete(filename)
            try:
                fs.delete(filename+"--journal")     
            except Exception as e:
                print(str(e))
        return redirect("telegram_dm_bot")
    else:
        return HttpResponse("please log in first")

def edit_telegram_account(request,id):
    if request.session['is_login'] is True:
        if request.method =='POST':
            hash_id = request.POST.get("hash_id")
            hash_key = request.POST.get("hash_key")
            number = request.POST.get("number")
            sleep_time = request.POST.get("sleep_time")
            sleep_time_first = request.POST.get("sleep_time_first")
            session_file = request.FILES.get("session_file")
            t = Telegram_Accounts.objects.get(id=id) 
            if session_file:
                old_filename = Telegram_Accounts._meta.get_field('session_file').value_from_object(Telegram_Accounts.objects.get(id=id)) 
                if old_filename:
                    fs = FileSystemStorage(location=TELEGRAM_SESSIONS_FOLDER) #defaults to   MEDIA_ROOT  
                    old_filename = fs.delete(old_filename)
                filename = session_file.name
                filename = filename.replace("+","")
                fs = FileSystemStorage(location=TELEGRAM_SESSIONS_FOLDER) #defaults to   MEDIA_ROOT  
                filename = fs.save(filename,session_file)
                file_url = fs.url(filename)
                t.hash_id = hash_id
                t.hash_key = hash_key
                t.number = number
                t.session_file = filename
                t.sleep_time = sleep_time
                t.sleep_time_first = sleep_time_first
                t.save()
            else: 
                t.hash_id = hash_id
                t.hash_key = hash_key
                t.number = number
                t.sleep_time = sleep_time
                t.sleep_time_first = sleep_time_first
                t.save()
            return redirect("telegram_dm_bot")
        data = Telegram_Accounts.objects.all().filter(id=id)
        user_data = User.objects.all().filter(id=request.session.get('userid'))
        context = {"user_data":user_data,"data":data}
        return render(request,'telegramBot/edit-telegram-account.html',context)
        return redirect("telegram_dm_bot")
    else:
        return HttpResponse("please log in first")

def delete_telegram_groups(request,id):
    if request.session['is_login'] is True:
        account_id = Telegram_Groups._meta.get_field('account_id').value_from_object(Telegram_Groups.objects.get(id=id))
        Telegram_Groups.objects.filter(id=id).delete()
        return redirect("/telegramBot/telegram-dmBot-send/"+str(account_id)+"/1")
    else:
        return HttpResponse("please log in first")

def delete_telegram_questions(request,id):
    if request.session['is_login'] is True:
        account_id = Telegram_Questions._meta.get_field('account_id').value_from_object(Telegram_Questions.objects.get(id=id))
        Telegram_Questions.objects.filter(id=id).delete()
        return redirect("/telegramBot/telegram-dmBot-send/"+str(account_id)+"/1")
    else:
        return HttpResponse("please log in first")

def delete_telegram_answers(request,id):
    if request.session['is_login'] is True:
        account_id = Telegram_Answers._meta.get_field('account_id').value_from_object(Telegram_Answers.objects.get(id=id))
        Telegram_Answers.objects.filter(id=id).delete()
        return redirect("/telegramBot/telegram-bot-send/answer/"+str(account_id)+"/1")
    else:
        return HttpResponse("please log in first")

def coming_soon(request):
    user_data = User.objects.all().filter(id=request.session.get('userid'))
    context = {"user_data":user_data,"username":request.session.get('username'),}
    return render(request,"telegramBot/coming-soon.html",context)

def schedule_messages(request):
    if request.session['is_login'] is True:
        user_data = User.objects.all().filter(id=request.session.get('userid'))
        messages = Schedule_Messages.objects.all().filter(userid = request.session.get('userid'))
        context = {"user_data":user_data,"messages":messages,"username":request.session.get('username')}
        return render(request,'telegramBot/schedule-messages.html',context)


    else:
        return HttpResponse("please log in first")

def delete_schedule_messages(request,id):
    if request.session['is_login'] is True:
        Schedule_Messages.objects.filter(id=id).delete()
        return redirect(schedule_messages)

    else:
        return HttpResponse("please log in first")

def time_now(request):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    tm_string = now.strftime("%H:%M")
    print("time-now = ",tm_string)
    return HttpResponse(tm_string)

