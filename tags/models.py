from django.db import models
from questions.models import Question

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('question', 'tag')

    def __str__(self):
        return f"{self.question.title} - {self.tag.name}"
