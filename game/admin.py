from django.contrib import admin
from EA.game.models import Game, Team

class teamInline(admin.TabularInline):
	model = Team
	extra = 2

class gameAdmin(admin.ModelAdmin):
	fields = ['name', 'players']
	inlines = [teamInline]

admin.site.register(Game, gameAdmin)
admin.site.register(Team)