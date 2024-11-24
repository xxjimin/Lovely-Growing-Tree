from django.db import models

class Letter(models.Model):
    tree_id = models.ForeignKey('Trees.Tree', on_delete=models.CASCADE)
    content = models.TextField()
    author_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('read', 'Read')], default='active')
    username = models.CharField(max_length=50)

    def __str__(self):
        return f"Letter from {self.author_name} to Tree {self.tree_id}"
