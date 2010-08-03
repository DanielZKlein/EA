from django.shortcuts import render_to_response, redirect, get_object_or_404
from EA.chat.models import Chat
from django.http import HttpResponse

def chatsay(request, chatid):
	mychat = Chat.objects.get(pk=chatid)
	mychat.say(request.user, request.GET['text'])
	return HttpResponse('')