from django.contrib import admin
from django.utils.html import format_html
from django import forms

from .models import SingleWordsSituation, SingleWordsVideos


class SingleWordsSituationAdminForm(forms.ModelForm):
    class Meta:
        model = SingleWordsSituation
        fields = ['word', 'image', 'sound_type', 'syllables']
        help_texts = {
            'syllables': '''Beispiele: <br>
                            Wort: Wasserflasche <br>
                            Silben: Was, ser, fla, sche <br>
                            --- <br>
                            Wort: Baum <br>
                            Silben: Baum'''
        }

    def __init__(self, *args, **kwargs):
        super(SingleWordsSituationAdminForm, self).__init__(*args, **kwargs)
        self.fields['word'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['image'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['syllables'].widget.attrs.update({'autocomplete': 'off'})

class SingleWordAdmin(admin.ModelAdmin):
    form = SingleWordsSituationAdminForm



    list_display = ('word', 'sound_type', 'image_tag', 'syllables')
    fields = ('word', 'image', 'sound_type', 'syllables')  # Display fields
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
