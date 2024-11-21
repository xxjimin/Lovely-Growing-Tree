from django.db import models
from django.contrib.auth.models import User

# Users 테이블
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)  # 자동 증가 필드
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.username

# Trees 테이블
class Trees(models.Model):
    tree_name = models.CharField(max_length=50)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tree_name

# Letters 테이블
class Letters(models.Model):
    tree = models.ForeignKey(Trees, on_delete=models.CASCADE)
    content = models.TextField()
    author_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Letter by {self.author_name} on {self.created_at}"

# Ornaments 테이블
class Ornaments(models.Model):
    tree = models.ForeignKey(Trees, on_delete=models.CASCADE)
    position_x = models.FloatField()
    position_y = models.FloatField()
    letter = models.ForeignKey(Letters, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Ornament at position ({self.position_x}, {self.position_y})"
