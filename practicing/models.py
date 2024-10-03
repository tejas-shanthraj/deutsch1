from django.db import models

class PracticingSituation(models.Model):

    LANG_CHOICES = {
        ('en-US','English')
    }

    topic = models.CharField(max_length=250)
    about = models.CharField(max_length=400)
    participants = models.CharField(max_length=250)
    student_role = models.CharField(max_length=150)
    student_goal = models.CharField(max_length=150)
    lang = models.CharField(max_length=150, choices = LANG_CHOICES)

    questions = models.JSONField(blank=True, null=True, default = {})

    def __str__(self):
        return self.topic
