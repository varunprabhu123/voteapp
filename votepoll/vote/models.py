from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class VotePoll(models.Model):
    candidate_name=models.CharField(max_length=100)
    party_name=models.CharField(max_length=100)
    vote=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.party_name
    
class VoterRecord(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    has_voted=models.BooleanField(default=False)

    def __str__(self):
        return self.user_name

