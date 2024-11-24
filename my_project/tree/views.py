from django.http import JsonResponse
from .models import Tree

def list_trees(request):
    trees = Tree.objects.all().values()
    return JsonResponse(list(trees), safe=False)

def create_tree(request):
    # Handle creation logic
    pass
