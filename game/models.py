from django.db import models
from django.contrib.auth.models import User
from EA.chat.models import Chat
from EA.tools import dbug
from django.contrib.contenttypes import generic

# Create your models here.

class Team(models.Model):
	players = models.ManyToManyField(User, blank=True)
	# chat = generic.GenericRelation(Chat)
	chat = models.OneToOneField(Chat, related_name="team_chat", null = True)

	def join(self, user):
		if user in self.players.all():
			return False
		self.players.add(user)
		self.chat.join(user)
		return True
		
	def leave(self, user):
		if not user in self.players.all():
			return False
		self.players.remove(user)
		self.chat.leave(user)
		return True
		


class Game(models.Model):
	name = models.CharField(max_length=100)
	opened_date = models.DateTimeField(auto_now_add=True)
	players = models.ManyToManyField(User)
	team1 = models.OneToOneField(Team, related_name="team1", null=True)
	team2 = models.OneToOneField(Team, related_name="team2", null=True)
	# these fields need to be filled when a new game is created :(
	max_players = models.IntegerField(default=8)
	status = models.CharField(max_length=10, default="Lobby")
	chat = models.OneToOneField(Chat, related_name="chat", null = True)
	
	def __unicode__(self):
		return self.name

	def user_inside(self, user):
		return user in self.players.all()
		
	def join(self, user):
		if user in self.players.all() or self.players.count() >= self.max_players:
			return False
		else:
			self.players.add(user)
			self.chat.join(user)
			numt1users = len(self.team1.players.all())
			numt2users = len(self.team2.players.all())
			if numt1users > numt2users:
				self.team2.join(user)
			else:
				self.team1.join(user)
			return True
			
	def leave(self, user):
		if not user in self.players.all():
			return False
		self.players.remove(user)
		self.chat.leave(user)
		self.team1.leave(user)
		self.team2.leave(user)
		return True

class A(models.Model):
	nameshmame = models.CharField(max_length=100, null=True)
	myB = models.OneToOneField("B", related_name="thisb")
	otherB = models.OneToOneField("B", related_name="thisotherb")
	
class B(models.Model):
	name = models.CharField(max_length=100, null=True)

	def __unicode__(self):
		return self.name