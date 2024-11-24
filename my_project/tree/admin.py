from django.contrib import admin
from .models import Tree

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')
    search_fields = ('name', 'owner__username')
