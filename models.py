# myapp/models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# Trees 테이블 모델
class Tree(models.Model):
    tree_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'trees'  # MySQL 테이블명과 매칭
        managed = False  # Django에서 이 테이블을 관리하지 않도록 설정

    def __str__(self):
        return self.tree_name


# Letters 테이블 모델
class Letter(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    content = models.TextField()
    author_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'letters'  # MySQL 테이블명과 매칭
        managed = False  # Django에서 이 테이블을 관리하지 않도록 설정

    def __str__(self):
        return f"Letter from {self.author_name} to {self.tree.tree_name}"
