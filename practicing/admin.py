from django.contrib import admin

from .models import PracticingSituation

class SituationAdmin(admin.ModelAdmin):
    list_filter = ("lang", "topic")
    list_display = ("topic", "lang",)
    # prepopulated_fields = {"slug": ("topic",)}

admin.site.register(PracticingSituation, SituationAdmin)
