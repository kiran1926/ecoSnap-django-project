from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Sighting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    species_name = models.CharField(max_length=200, help_text="e.g., Oak Tree, Dandelion, Tall Fescue Grass")
    description = models.TextField(blank=True, help_text="Notes about the sighting, habitat, etc.")
    latitude = models.FloatField()
    longitude = models.FloatField()
    image_urls = models.TextField(blank=True, help_text="URLs of images from Supabase, one per line.") 
    is_native = models.BooleanField(null=True, blank=True, help_text="Is this species native to this location?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.species_name} sighted by {self.user.username} at ({self.latitude:.2f}, {self.longitude:.2f})"

    def get_absolute_url(self):
        return reverse('main_app:sighting_detail', kwargs={'sighting_id': self.id})

    class Meta:
        ordering = ['-created_at']
