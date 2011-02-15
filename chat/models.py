from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from EA.tools import dbug

class UserActivity(models.Model):
	user = models.ForeignKey(User)
	chat = models.ForeignKey('Chat')
	ping = models.DateTimeField(auto_now=True)

class Chat(models.Model):
	users = models.ManyToManyField(User)
	created = models.DateTimeField(auto_now_add = True)
	
	def join(self, joiner):
		if joiner in self.users.all():
			# already in chat
			return False
		self.action(joiner, "join")
		self.users.add(joiner)
		return True
		
	def leave(self, leaver):
		if leaver not in self.users.all():
			# not in chat
			return False
		self.action(leaver, "leave")
		self.users.remove(leaver)
		return True
	
	def action(self, actor, action, more_info={}):
		dbug("received action! Actor is " + actor.username + " and action is " + action)
		if actor not in self.users.all() and action != "join":
			dbug("bailing because user is not in and action is not join")
			return False
		if action == "join" and actor in self.users.all():
			return False # joining but already in chat
		if action == "leave" and action not in self.users.all():
			return False # leaving, but not in chat
		# We are handling max users on a higher level, based on the object this chat belongs to
		# So a game needs to check that a user does not exceed its max users. By the time
		# a higher level object calls a chat, we assume that the max users check is done.
		if action == "join":
			dbug("creating line...")
			self.line_set.create(is_action=True, user=actor, text="join")
			return True
		if action == "leave":
			self.line_set.create(is_action=True, user=actor, text="leave")
			return True
	
	def emote(self, emo, what):
		if emo not in self.users.all():
			return False
		self.line_set.create(text=what, user=emo, is_emote=True)
		return True
	
	def say(self, speaker, text):
		if speaker not in self.users.all():
			return False
		self.line_set.create(text=text, user=speaker)
		return True
		
	def listen(self, userlistening, start=0):
		""" Returns a number of line objects """
		if userlistening not in self.users.all():
			dbug("User " + userlistening.username + " is not in chat " + str(self.id))
			return False
		return self.line_set.filter(pk__gt=start)
		
class Line(models.Model):
	text = models.CharField(max_length=1000)
	is_emote = models.BooleanField(default = False) # is this a /me?
	is_action = models.BooleanField(default = False) # is this an action? (join, leave)
	user = models.ForeignKey(User)
	chat = models.ForeignKey(Chat, null=True)
	timestamp = models.DateTimeField(auto_now_add = True)
	
	def __unicode__(self):
		return self.format_for_output("text")
	
	def get_timestamp(self):
		return "["+self.timestamp.strftime("%H:%M:%S")+"]"
	
	def format_for_output(self, format="ajax"):
		if not self.is_action and not self.is_emote:
			if format == "ajax":
				return [["say", self.get_timestamp() + " &lt;"+self.user.username+"&gt; " + htmlify(self.text) + "<br>"]]
			if format == "text":
				return self.get_timestamp() + " <"+self.user.username+"> " + self.text + "\n"
		if self.is_action:
			if format == "ajax":
				ro = []
				if self.text == "join":
					ro.append([self.text, self.user.id, self.user.username, "online"])
					ro.append(["say", self.get_timestamp() + " " + self.user.username + " has joined the chat.<br>"])
				if self.text == "leave":
					ro.append([self.text, self.user.id])
					ro.append(["say", self.get_timestamp() + " " + self.user.username + " has left the chat.<br>"])
				return ro
			if format == "text":
				return self.get_timestamp() + " User " + self.user.username + " performed action: " + self.text
		if self.is_emote:
			if format == "ajax":
				return ["say", self.get_timestamp() + " * " + self.user.username + " " + htmlify(self.text) + "<br>"]
			if format == "text":
				return self.get_timestamp() + " * " + self.user.username + " " + self.text

				
def htmlify(string):
	newstring = string.replace("<", "&lt;")
	newstring = newstring.replace(">", "&gt;")
	return newstring