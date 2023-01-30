# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import requests
from .forms import FormContactForm


#index
def index(request):
	return render(request, 'user/index.html', {'title':'index'})

#register here 
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			##mail system
			htmly = get_template('user/Email.html')
			d = { 'username': username }
			subject, from_email, to = 'welcome', 'hozefaabbas1911@gmail.com', email
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			
			messages.success(request, f'Your account has been created ! You are now able to log in')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'user/register.html', {'form': form, 'title':'register here'})


def Login(request):
	if request.method == 'POST':

		# AuthenticationForm_can_also_be_used__

		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {username} !!')
			return redirect('index')
		else:
			messages.info(request, f'account done not exit plz sign in')
	form = AuthenticationForm()
	return render(request, 'user/login.html', {'form':form, 'title':'log in'})

def news(request):
    url = 'https://newsapi.org/v2/everything?q=mentalhealth&sortBy=popularity&apiKey=e21c28ebd4ff471e970182ebc9da81fd'
    latest_news = requests.get(url).json()
    a = latest_news['articles']
    desc =[]
    title =[]
    img =[]
    for i in range(len(a)):
        f = a[i]
        title.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])
    mylist = zip(title, desc, img)
    context = {'mylist': mylist}
    return render(request, 'News\index4.html', context)

	
def homepage(request):
	
    return render(request,'index.html')
def maps(request):
      
    return render(request,'maps.html')
def contactus(request):
	form= FormContactForm(request.POST or None)
	if form.is_valid():
		form.save()
	context= {'form': form }
	return render(request, 'contact.html', context)

        
   

