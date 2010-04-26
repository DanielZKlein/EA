from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from EA.game.models import Game

def get_standard_dict(request):
	standard_dict = {'loggedin' : request.user.is_authenticated(), 'username' : request.user.username}
	return standard_dict

def rootview(request, message=None):
	games_to_show = Game.objects.filter(status__in=["Lobby", "Running"])
	for tempgame in games_to_show:
		if tempgame.user_inside(request.user):
			tempgame.currentlyin = True			
		else:
			tempgame.currentlyin = False
			if tempgame.players.count() < tempgame.max_players:
				tempgame.canbejoined = True
			else:
				tempgame.canbejoined = False
		
	sd = get_standard_dict(request)
	sd['games'] = games_to_show
	return render_to_response('templates/rootview.html', sd)

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