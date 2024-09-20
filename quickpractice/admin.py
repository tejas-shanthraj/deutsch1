from django.contrib import admin

# Register your models here.
from .models import Sentences, Words

class QuickPracticeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sentences, QuickPracticeAdmin)
admin.site.register(Words, QuickPracticeAdmin)
