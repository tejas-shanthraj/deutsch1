from django.contrib import admin

from .models import SingleWordsSituation

class SituationAdmin(admin.ModelAdmin):
    # list_filter = ("lang", "topic")
    # list_display = ("topic", "lang",)
    # prepopulated_fields = {"slug": ("topic",)}
    None

admin.site.register(SingleWordsSituation, SituationAdmin)