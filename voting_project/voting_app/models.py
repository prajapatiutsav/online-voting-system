from django.db import models
from django.contrib.auth.models import User


# 🗳️ Candidate Model
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.party})"


# 🗳️ Vote Model (1 user = 1 vote)
class Vote(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} voted for {self.candidate.name}"


# ⚙️ Election Control Model
class ElectionControl(models.Model):
    show_results = models.BooleanField(default=False)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Election Settings"
