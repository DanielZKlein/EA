from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from EA.game.models import Game
from EA.chat.models import Chat
from django.http import HttpResponse
import json, re
from EA.tools import dbug

def get_standard_dict(request):
	standard_dict = {'loggedin' : request.user.is_authenticated(), 'username' : request.user.username}
	return standard_dict

def ajax(request):
	if not request.is_ajax():
		return False
	# dbug("handling ajax request")
	# dbug(request.GET)
	chatrefreshpattern = re.compile(r'^chat(\d+)refresh$')
	playerspattern = re.compile(r'^players(\d)refresh$')
	returnObject = { "chatqueues" : {}, "playerupdates" : {}}
	for key in request.GET:
		m = chatrefreshpattern.search(key)
		if m:
			chatid = m.group(1)
			lastrefresh = request.GET[key]
			mychat = Chat.objects.get(pk=chatid)
			lines = mychat.listen(request.user, lastrefresh)
			newlast = 0
			saytext = ""
			returnObject["chatqueues"][chatid] = []
			hadLines = False
			for line in lines:
				hadLines = True
				formatted_line = line.format_for_output()
				newlast = line.id
				for fline in formatted_line:
					#may be more than one line per return
					returnObject["chatqueues"][chatid].append(fline)
			if hadLines: 
				returnObject["chatqueues"][chatid].append(["newlastid", newlast])
		else:
			m = playerspattern.search(key)
			if m:
				gameid = m.group(1)
				mygame = Game.objects.get(pk=gameid)
				dbug(mygame)
				tempdic = {}
				team1 = []
				team2 = []
				for player in mygame.team1.players.all():
					team1.append(player.username)
				for player in mygame.team2.players.all():
					team2.append(player.username)
				tempdic["team1"] = team1
				tempdic["team2"] = team2
				returnObject["playerupdates"][gameid] = tempdic
				dbug(tempdic)
	chatjson = json.dumps(returnObject)

	return HttpResponse(chatjson)
				
		
	
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