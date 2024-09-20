from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import SingleWordsSituation, SingleWordsVideos

class SingleWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'sound_type', 'image_tag')
    fields = ('word', 'image', 'sound_type')  # Display fields
    list_filter = ['sound_type']
    readonly_fields = ('image_tag',)  # Display image thumbnail in admin

    def image_tag(self, obj):
        if obj.image:
            # return '<img src="/static/images/singlewords/{}" width="50" height="50" />'.format(obj.image.name)
            return format_html('<img src="/static/images/singlewords/{}" width="50" height="50" />', obj.image)
        
        else:
            return 'No image uploaded'
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
admin.site.register(SingleWordsSituation, SingleWordAdmin)



class VideoAdmin(admin.ModelAdmin):
    None
admin.site.register(SingleWordsVideos, VideoAdmin)
