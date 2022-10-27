from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class CustomUser(AbstractUser):
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.username

    # def save(self):
    #     super().save()
    #
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class Relations(models.Model):
    initiator = models.ForeignKey(CustomUser, related_name='initiated_relations', on_delete=models.SET('User Deleted'))
    receiver = models.ForeignKey(CustomUser, related_name='received_relations', on_delete=models.SET('User Deleted'))

    # Can't add same relation twice:
    class Meta:
        unique_together = ('initiator', 'receiver',)


class Messages(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='send_messages')
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    body = models.TextField()
    send = models.DateTimeField(default=timezone.now)
