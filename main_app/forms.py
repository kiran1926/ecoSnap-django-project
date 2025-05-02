from django import forms
from .models import Sighting

class SightingForm(forms.ModelForm):
    image_urls = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter image URLs from Supabase, one per line.'}), required=False, help_text="After uploading images to Supabase, paste the URLs here, one per line.")
    latitude = forms.FloatField(widget=forms.HiddenInput()) 
    longitude = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Sighting
        fields = [
            'species_name',
            'description',
            'latitude',
            'longitude',
            'image_urls',
            'is_native'
        ]
        widgets = {
            'species_name': forms.TextInput(attrs={'placeholder': 'e.g., Monarch Butterfly, Oak Tree'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your sighting, the habitat, weather, etc.'}),
            'is_native': forms.Select(choices=((None, 'Unknown'), (True, 'Yes'), (False, 'No')))
        }
        help_texts = {
            'species_name': 'What species did you observe?',
            'is_native': 'Is this species native to the location of the sighting?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_native'].label = "Is this species native to this location?"