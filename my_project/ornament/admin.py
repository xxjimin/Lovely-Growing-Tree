from django.contrib import admin
from .models import Ornament

@admin.register(Ornament)
class OrnamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'tree_id', 'letter_id', 'position_x', 'position_y')
    search_fields = ('tree_id__name',)
