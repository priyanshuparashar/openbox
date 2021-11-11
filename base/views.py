from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Rooms, Topic, Message, Contact
import requests
from bs4 import BeautifulSoup
import pandas as pandu
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomsForm
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# mylist =[
#     {'id':1,'name': 'xyz'},
#     {'id': 2,'name': 'abc'}
# ]
@login_required(login_url='loginr')
def contact(request):
    if request.method == 'POST':
            contact = Contact.objects.create(
            sender=request.user,
            c_email=request.POST.get('c_email'),
            c_message=request.POST.get('c_message')
            )
    return render(request, 'contact.html')
            
    
       
            

      
        
    



# to be completed, login and signup is still remaining 
def loginr(request):
    page =  'login'

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        uname = request.POST.get('username')
        passs = request.POST.get('password')
        try:
            user = User.objects.get(username=uname)
            
        except:
            messages.error(request, '{} does not exist'.format(uname))

        user=authenticate(request,username=uname, password=passs)   
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username password does not exist')

    context = {'page':page}
   
    return render(request,'loginr.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
           user = form.save()
           login(request, user)
           return redirect('home')
        
            
    
    return render(request, 'loginr.html',{'form':form} )
# this below is view for home page ( index page )
# search functionlaity is implemented using if conditions to overcome the bug of empty get request 
def home(request):
    
    

    q = request.GET.get('q')
    if request.GET.get('q') == None:
        rooms = Rooms.objects.all()
    else:
        rooms = Rooms.objects.filter(
            Q(topic__name__icontains=q) |
            Q(description__icontains=q) 
            
            
        )

             

        

    
    # rooms = Rooms.objects.filter(topic__name=q) 
    topics = Topic.objects.all()
   
    
    
   
    message = Message.objects.all()
    context={'mylist':rooms,'topic':topics, 'message':message}
    

    return render(request,'home.html', context)


def tests(request):
    return render(request, 'test1.html')

def userprofile(request, pk):
    user = User.objects.get(id=pk)
    room = user.rooms_set.all()
    c = user.rooms_set.all().count()
    message = Message.objects.all()
    topic = Topic.objects.all

    print(c)
    return render(request, 'userprofile.html', {'user': user, 'mylist':room, 'topic':topic, 'count':c, 'message':message})
    
    
    # rooms = user.room_set.all()
    # room_message = user.message_set.all()
    # topics = Topic.objects.all()
    # context = {
    #     'user': user,
    #     'rooms': room,
    #     'room_message': room_message,
    #     'topics':topics
    # }
    # return render(request, 'userprofile.html', context)

# this room view below displays the rooms on individual page by using id
def room(request, pk):
    
    room = Rooms.objects.get(id=pk)
    conv = room.message_set.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        return redirect('room', pk=room.id)

   
    

    
    print(conv)
   # print(conv.user)
    
    #print(room.description)
    # content={'room':room}
    return render(request,'room.html',{'room':room,'desc':room.description, 'conv':conv  })
# Create your views here.

# import requests
# from bs4 import BeautifulSoup
# import pandas as pandu

#import the library to query a website
#specify the url
# web view below is a test of web scrapping integration in web app 
# here beautiful soup and pandas and request is used 
# data is fetched from wiki list of asian contries
def web(request):
    wiki_link="https://en.wikipedia.org/wiki/List_of_Asian_countries_by_area"
    link=requests.get(wiki_link).text;
    soup=BeautifulSoup(link, 'lxml');
# temp=soup.find_all('table');
# for t in temp:
#     print(t.get('title'));
    all_table=soup.find_all('table')
    right_table=soup.find('table', class_="wikitable sortable")
    finaltemp=right_table.find_all('a')
    goku=[];
    for p in finaltemp:
      goku.append(p.get('title'));

    df=pandu.DataFrame()
    df['country']=goku
    # print(df)
    
   
    df.to_excel('result.xlsx')
    myl={'my':goku}
    print(myl)
    print(goku)
    return render(request, 'test.html', {'my': goku})
    
# createroom is a view used for geting data from form to crear rooms and store that on database
@login_required(login_url='loginr')
def createroom(request):
    form = RoomsForm()
    if request.method == 'POST':
        form = RoomsForm(request.POST)
        if form.is_valid():
            
            
            form.save()
        
    context={'form':form}
    return render(request, 'room_form.html',context)

# update room view is used to update data  
@login_required(login_url='loginr')  
def updateroom(request,pk):
    room = Rooms.objects.get(id=pk)
    form = RoomsForm(instance=room)

    if request.user != room.host:
        return HttpResponse('you cant update {}"s room'.format(room.host))

    if request.method == 'POST':
        form = RoomsForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            return redirect('home')

    
    return render(request, 'room_form.html', {'form': form})
@login_required(login_url='loginr')
def deleteroom(request,pk):
    room = Rooms.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('you cant delete {}"s room'.format(room.host))
        
    if request.method == 'POST':
        room.delete() #in built function in django 
        return redirect('home')
    return render(request, 'delete.html', {'obj':room})




        

     

