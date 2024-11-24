from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Letter

def list_letters(request):
    letters = Letter.objects.all().values()
    return JsonResponse(list(letters), safe=False)

def create_letter(request):
    # Handle creation logic
    pass
