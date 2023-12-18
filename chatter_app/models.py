from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_requests"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_requests"
    )
    is_accepted = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    friends = models.ManyToManyField(User, related_name="friend", blank=True)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.sender.profile.friends.filter(pk=self.receiver.pk).exists():
            super().save(*args, **kwargs)
        else:
            raise ValidationError("You can only send messages to your friends.")
