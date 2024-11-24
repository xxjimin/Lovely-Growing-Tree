from django.db import models

class Tree(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey('Users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"Tree {self.name} owned by {self.owner.username}"
