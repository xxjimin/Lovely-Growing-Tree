from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Ornament

def list_ornaments(request):
    ornaments = Ornament.objects.all().values()
    return JsonResponse(list(ornaments), safe=False)

def create_ornament(request):
    # Handle creation logic
    pass
