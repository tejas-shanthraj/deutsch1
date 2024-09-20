from django.contrib import admin

# Register your models here.
from .models import LlmPrompt

class VoiceAssistantAdmin(admin.ModelAdmin):
    pass

admin.site.register(LlmPrompt, VoiceAssistantAdmin)
