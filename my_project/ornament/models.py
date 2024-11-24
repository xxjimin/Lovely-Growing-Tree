
# Create your models here.
from django.db import models

class Ornament(models.Model):
    tree_id = models.ForeignKey('Trees.Tree', on_delete=models.CASCADE)
    letter_id = models.ForeignKey('Letters.Letter', on_delete=models.CASCADE)
    position_x = models.FloatField()
    position_y = models.FloatField()

    def __str__(self):
        return f"Ornament on Tree {self.tree_id}"
