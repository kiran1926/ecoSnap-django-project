# ecoSnap

![ecoSnap Logo](https://images.pexels.com/photos/3228762/pexels-photo-3228762.jpeg?auto=compress&cs=tinysrgb&w=600)

## Overview

ecoSnap is a web application built with Django that allows users to log, view, and manage sightings of flora and fauna. Users can record observations, view them on an interactive map, and get AI-powered analysis for plant images.

### Why ecoSnap?

In today's world, understanding and preserving our local ecosystems is more important than ever. ecoSnap was built to make it easier for nature enthusiasts, researchers, and everyday citizens to document and learn about the plants and wildlife around them. By combining modern technology with environmental awareness, we aim to create a community-driven platform for ecological discovery and education.

## Getting Started

- [Live Demo](https://ecosnap-1679702835f6.herokuapp.com/)
- [Project Planning](https://github.com/kiran1926/ecoSnap-django-project)

## Features

The application includes the following key features:

- **[Index Page](./documentation/index_page.md)**: Landing page that directs authenticated users to the map and new users to sign up/login.
- **[User Signup](./documentation/user_signup.md)**: Allows new users to register for an account.
- **[Sighting Map View](./documentation/sighting_map_view.md)**: Displays all sightings on an interactive map for authenticated users.
- **[Sighting Detail View](./documentation/sighting_detail_view.md)**: Shows detailed information for a single sighting.
- **[Sighting Creation](./documentation/sighting_creation.md)**: Allows authenticated users to add new sightings, including location, description, and images.
- **[Sighting Update](./documentation/sighting_update.md)**: Enables users to edit their existing sightings.
- **[Sighting Deletion](./documentation/sighting_deletion.md)**: Allows users to delete their own sightings after confirmation.
- **[Image Analysis API](./documentation/image_analysis_api.md)**: An API endpoint that uses OpenAI's Vision API to analyze plant images and return information like species name, description, and native status.

## Model Schema

### Sighting Model
```python
class Sighting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    species_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image_urls = models.TextField(blank=True)
    is_native = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
```

### Field Descriptions
- `user`: Foreign key to Django's built-in User model
- `species_name`: Name of the observed species (max 200 characters)
- `description`: Optional detailed description of the sighting
- `latitude`: Geographic latitude coordinate
- `longitude`: Geographic longitude coordinate
- `image_urls`: Text field storing image URLs (one per line)
- `is_native`: Boolean indicating if the species is native to the location
- `created_at`: Timestamp of when the sighting was created
- `updated_at`: Timestamp of when the sighting was last updated

## Technologies Used

- **Backend**: 
  - Python 3.x
  - Django 5.2
  - PostgreSQL
- **Frontend**: 
  - HTML5
  - CSS3 (Tailwind CSS)
  - JavaScript
- **APIs**:
  - Mapbox (for interactive maps)
  - OpenAI GPT-4 Vision API (for image analysis)
- **Other Libraries**: 
  - `requests` (for making HTTP requests to OpenAI)
  - `python-dotenv` (for environment variable management)

## Attributions

- Images: [Pexels](https://www.pexels.com/) (Free to use)
- Icons: [Heroicons](https://heroicons.com/) (MIT License)
- Map Integration: [Mapbox](https://www.mapbox.com/)
- AI Analysis: [OpenAI](https://openai.com/)

## Next Steps

Future enhancements planned for ecoSnap include:

1. **Community Features**:
   - User profiles with activity history
   - Comments and discussions on sightings
   - Follow other users and their discoveries

2. **Advanced AI Features**:
   - Real-time plant identification
   - Seasonal change tracking
   - Invasive species detection

3. **Mobile Experience**:
   - Progressive Web App (PWA) support
   - Offline data collection
   - Push notifications for nearby sightings

4. **Data Analysis**:
   - Species distribution maps
   - Seasonal trends visualization
   - Environmental impact assessment

5. **Educational Tools**:
   - Species information database
   - Guided nature walks
   - Citizen science projects integration

For detailed information on each feature, please refer to the linked documentation files.

