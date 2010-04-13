from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout

def get_standard_dict(request):
	standard_dict = {'loggedin' : request.user.is_authenticated(), 'username' : request.user.username}
	return standard_dict

def rootview(request, message=None):
	return render_to_response('templates/rootview.html', {'loggedin' : request.user.is_authenticated(), 'username': request.user.username})

def private(request):
	if not request.user.is_authenticated():
		request.session['forward_to'] = request.path
		return render_to_response('templates/loginpage.html', {'error': "The page you requested (" + request.path + ") requires login."})
	standard_dict = get_standard_dict(request)
	return render_to_response('templates/private.html', standard_dict)
	
def public(request):
	sd = get_standard_dict(request)
	return render_to_response('templates/public.html', sd)
	
def publicsecret(request):
	sd = get_standard_dict(request)
	return render_to_response('templates/publicsecret.html', sd)
	
def loginpage(request, error=None):
	return render_to_response('templates/loginpage.html', {'error' : error})
	
def dologin(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is None:
		return render_to_response('templates/loginpage.html', {'error' : 'Incorrect user/password'}) 
	login(request, user)
	if request.session.get('forward_to', False):
		return redirect(request.session['forward_to'])
	return redirect(rootview)
	
def dologout(request):
	logout(request)
	return redirect(rootview)