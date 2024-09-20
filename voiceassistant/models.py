from django.db import models

# Create your models here.
class LlmPrompt(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    prompt_type = models.CharField(max_length=20, default='None')
    input_prompt = models.TextField(default='')

    def __str__(self):
        return self.input_prompt
