from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

class Question(models.Model):
    topic_description = models.CharField(max_length=1000)
    publication_date = models.DateTimeField('date published')

    def __str__(self):
        return self.topic_description

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.publication_date <= now

    was_published_recently.admin_order_field = 'publication_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING,)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text