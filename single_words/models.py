from django.db import models
from django.core.files.storage import FileSystemStorage

# Define a file system storage to point to static folder
static_storage = FileSystemStorage(location='static/images/singlewords/')


class SingleWordsVideos(models.Model):
    sound_type = models.CharField(max_length=250, unique=True)
    url = models.URLField()
    

    def __str__(self):
        return f"{self.sound_type}"


class SingleWordsSituation(models.Model):
    word = models.CharField(max_length=250)
    image = models.ImageField(storage=static_storage)  # Image upload
    sound_type = models.ForeignKey(SingleWordsVideos, on_delete=models.CASCADE, db_column='sound_type')
    syllables = models.CharField(max_length=500, blank=False, null=True)

    def __str__(self):
        return f"{self.word}"

