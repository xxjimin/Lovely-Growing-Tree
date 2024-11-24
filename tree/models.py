from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Tree(models.Model):
    tree_id = models.AutoField(primary_key=True)
    tree_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tree')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tree_name


class Letter(models.Model):
    letter_id = models.AutoField(primary_key=True)  # letter_id 필드를 명시적으로 지정
    content = models.TextField()
    author_name = models.CharField(max_length=50)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author_name



class Ornament(models.Model):
    ornament_id = models.AutoField(primary_key=True)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE)
    position_x = models.FloatField()
    position_y = models.FloatField()

    def __str__(self):
        return f"Ornament on {self.tree.tree_name}"
