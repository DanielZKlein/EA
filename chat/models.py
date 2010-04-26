from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Chat(models.Model):
	name = models.CharField(max_length=30, null=True)
	users = models.ManyToManyField(User)
	created = models.DateTimeField(auto_now_add = True)
	content_type = models.ForeignKey(ContentType, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = generic.GenericForeignKey()
	
	def join(self, joiner):
		if joiner in self.users.all():
			# already in chat
			return False
		self.users.add(joiner)
		return True
		
	def leave(self, leaver):
		if leaver not in self.users.all():
			# not in chat
			return False
		self.users.remove(leaver)
		return True
	
	def __unicode__(self):
		return self.name
	
	def say(self, speaker, text):
		if speaker not in self.users.all():
			return False
		self.line_set.create(text=text, user=speaker)
		return True
		
	def listen(self, userlistening, start=0):
		""" Returns a number of line objects """
		if userlistening not in self.users.all():
			return False
		return self.line_set.filter(pk__gt=start)
		
class Line(models.Model):
	text = models.CharField(max_length=1000)
	user = models.ForeignKey(User)
	chat = models.ForeignKey(Chat, null=True)
	timestamp = models.DateTimeField(auto_now_add = True)
	
	def __unicode__(self):
		return self.user.username + ": " + self.text
