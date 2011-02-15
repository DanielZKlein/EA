from django.shortcuts import render_to_response, redirect, get_object_or_404
from EA.game.forms import TestForm, GameForm
from EA.game.models import Game, Team
from EA.chat.models import Chat
from EA.tools import dbug

def get_standard_dict(request):
	standard_dict = {'loggedin' : request.user.is_authenticated(), 'username' : request.user.username}
	return standard_dict
	
def game(request, id=-1):
	mygame = get_object_or_404(Game, pk=id)
	sd = get_standard_dict(request)
	if not request.user.is_authenticated():
		sd['errormessage'] = "Must log in to see game."
		return render_to_response('templates/error.html', sd)
	if not request.user in mygame.players.all():
		if mygame.players.count() < mygame.max_players:
			mygame.join(request.user)
			sd['message'] = "Joined game " + str(mygame.name)
		else:
			sd['errormessage'] = "You cannot see this game because you are not in it. You cannot join this game because it is full. It seems you are shit out of luck."
			return render_to_response('templates/error.html', sd)
	sd['game'] = mygame
	sd['gamechat'] = mygame.chat
	sd['t1users'] = mygame.team1.players.all()
	sd['t2users'] = mygame.team2.players.all()
	
	return render_to_response('templates/game.html', sd)
	
def prelobby(request):
	if request.method == "POST":
		## CREATING GAME
		form = GameForm(request.POST)
		if form.is_valid():
			newgame = Game(name=form.cleaned_data['name'])
			newgame.status = "Lobby"
			gc = Chat()
			gc.save()
			newgame.chat = gc
			myteam1 = Team()
			myteam2 = Team()
			t1c = Chat()
			t2c = Chat()
			t1c.save()
			t2c.save()
			myteam1.chat = t1c
			myteam2.chat = t2c
			myteam1.save()
			myteam2.save()
			newgame.team1 = myteam1
			newgame.team2 = myteam2
			newgame.save()
			newgame.join(request.user)
			newgame.save()
			return redirect("/game/"+str(newgame.id))
			
			
	sd = get_standard_dict(request)
	sd['form'] = GameForm()
	return render_to_response('templates/prelobby.html', sd)