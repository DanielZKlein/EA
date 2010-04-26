from django.shortcuts import render_to_response, redirect, get_object_or_404
from EA.game.forms import TestForm, GameForm
from EA.game.models import Game, Team
from EA.chat.models import Chat

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
	return render_to_response('templates/game.html', sd)
	
def prelobby(request):
	if request.method == "POST":
		form = GameForm(request.POST)
		if form.is_valid():
			newgame = Game(name=form.cleaned_data['name'])
			team1 = newgame.team_set.create(name="Team 1")
			team2 = newgame.team_set.create(name="Team 2")
			newgame.status = "Lobby"
			newgame.save()
			newgame.players.add(request.user)
			newgame.save()
			gamechat = Chat(name="Chat for game " + form.cleaned_data['name'], content_object = newgame)
			gamechat.save() 
			gamechat.join(request.user)
			t1chat = Chat(name="Team 1 Chat", content_object = team1)
			t2chat = Chat(name="Team 2 Chat", content_object = team2)
			gamechat.save()
			t1chat.save()
			t2chat.save()
			return redirect("/game/"+str(newgame.id))
			
			
	sd = get_standard_dict(request)
	sd['form'] = GameForm()
	return render_to_response('templates/prelobby.html', sd)