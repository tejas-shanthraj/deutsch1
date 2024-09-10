from django.db import models

# Create your models here.

LEVEL_CHOICES = {
        ("A1", "A1"),
        ("A2", "A2"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("C1", "C1"),
        ("C2", "C2")
    }
class Sentences(models.Model):
    
    id = models.AutoField(primary_key = True, unique = True)
    sentence = models.TextField(default='', unique = True)
    en_translation = models.TextField(default='')
    lang = models.CharField(max_length = 6, default='')
    phonetic = models.TextField(default='')
    ipa = models.TextField(default='')
    category = models.TextField(default='')
    difficulty = models.CharField(max_length=2, choices = LEVEL_CHOICES, default='')

    def __str__(self):
        return self.sentence

class Words(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    word = models.TextField(default='', unique = True)
    en_translation = models.TextField(default='')
    lang = models.CharField(max_length=6, default='')
    phonetic = models.TextField(default='')
    ipa = models.TextField(default='')
    category = models.TextField(default='')
    difficulty = models.CharField(max_length=2, choices = LEVEL_CHOICES, default='')

    def __str__(self):
        return self.word