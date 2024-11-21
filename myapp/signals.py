from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Users

@receiver(post_save, sender=User)
def create_user_in_users_table(sender, instance, created, **kwargs):
    if created:  # 새 사용자가 생성될 때만 실행
        Users.objects.create(
            user_id=instance.id,
            username=instance.username,
            created_at=instance.date_joined,
        )
