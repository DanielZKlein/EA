from django.db import models
from django.contrib.auth.models import User
from EA.chat.models import Chat
from django.contrib.contenttypes import generic

# Create your models here.

class Game(models.Model):
	name = models.CharField(max_length=100)
	opened_date = models.DateTimeField(auto_now_add=True)
	players = models.ManyToManyField(User)
	max_players = models.IntegerField(default=8)
	status = models.CharField(max_length=10, default="Lobby")
	chat = generic.GenericRelation(Chat)
	def __unicode__(self):
		return self.name
	
	def user_inside(self, user):
		return user in self.players.all()
		
	def join(self, user):
		if user in self.players.all() or self.players.count() >= self.max_players:
			return False
		else:
			self.players.add(user)
			self.chat.all()[0].join(user)
			return True
			
	def leave(self, user):
		if not user in self.players.all():
			return False
		self.players.remove(user)
		self.chat.all()[0].leave(user)
		for myteam in self.team_set.all():
			myteam.leave(user)
		return True

class Team(models.Model):
	name = models.CharField(max_length=300)
	game = models.ForeignKey(Game)
	players = models.ManyToManyField(User, blank=True)
	chat = generic.GenericRelation(Chat)

	def __unicode__(self):
		return self.name

	def join(self, user):
		if user in self.players.all():
			return False
		self.players.add(user)
		self.chat.all()[0].join(user)
		return True
		
	def leave(self, user):
		if not user in self.players.all():
			return False
		self.players.remove(user)
		self.chat.all()[0].leave(user)
		return True
		
