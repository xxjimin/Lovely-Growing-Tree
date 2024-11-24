from django.http import JsonResponse
from .models import User

def list_users(request):
    users = User.objects.all().values()
    return JsonResponse(list(users), safe=False)

def create_user(request):
    # Handle creation logic
    pass
