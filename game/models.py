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

class Team(models.Model):
	name = models.CharField(max_length=30)
	game = models.ForeignKey(Game)
	players = models.ManyToManyField(User, blank=True)

	def __unicode__(self):
		return self.name	
