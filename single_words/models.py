from django.db import models

class SingleWordsSituation(models.Model):
    word = models.CharField(max_length=250)
    image = models.CharField(max_length=250)
    sound_type = models.CharField(max_length=250)

    def __str__(self):
        return self.word, self.image, self.sound_type
    
class SingleWordsVideos(models.Model):
    sound_type = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    

    def __str__(self):
        return self.url, self.sound_type

