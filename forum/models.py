from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Question(models.Model):
    Title = models.CharField(max_length=200)
    Body = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    Asked_By = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.Title

    def get_absolute_url(self):
        return reverse('question', kwargs={'pk': self.pk})

class Answer(models.Model):
    Body = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    Answered_By = models.ForeignKey(User, on_delete=models.CASCADE)
    Question_Answered = models.ForeignKey(Question, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    upvote = models.BooleanField(null=False)

    class Meta:
        unique_together = ['voter', 'question']

class AnswerVote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    upvote = models.BooleanField(null=False)

    class Meta:
        unique_together = ['voter', 'answer']