from django.contrib import admin
from .models import Letter

@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('id', 'tree_id', 'author_name', 'status', 'created_at')
    search_fields = ('author_name', 'content')
    list_filter = ('status',)
