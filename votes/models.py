from django.db import models
from users.models import CustomUser
from questions.models import Question, Answer
from articles.models import Article

class Vote(models.Model):
    VOTE_TYPES = [
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, null=True, blank=True, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        permissions = [
            ("can_vote", "Puede votar"),
        ]

    def __str__(self):
        return f"{self.vote_type} by {self.user.username}"
