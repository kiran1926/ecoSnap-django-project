# Sighting Map View Feature

## Overview

This document describes the Sighting Map View, which is the primary interface for users to see all recorded sightings on an interactive map. This feature is accessible only to authenticated users.

## Frontend Flow

1.  An authenticated user navigates to the `/map/` URL. This might happen directly or via a redirect (e.g., after login or from the index page if already authenticated).
2.  The `main_app/map_view.html` template is rendered by the backend and sent to the browser.
3.  The frontend JavaScript, presumably using a library like Mapbox GL JS (given the `mapbox_access_token` in the context), initializes an interactive map.
4.  The `sightings_json` data (provided in the template context) is parsed by the JavaScript. This JSON contains an array of sighting objects.
5.  For each sighting in the JSON data, a marker (or similar visual representation) is placed on the map at its specified latitude and longitude.
6.  Users can typically interact with the map (pan, zoom).
7.  Clicking on a sighting marker on the map is expected to either:
    *   Display a pop-up with basic information (like species name, truncated description, first image).
    *   Navigate the user to the Sighting Detail View for that specific sighting, using the `detail_url` provided for each sighting in the JSON data.

## Backend Processing

### URL Pattern

-   **Pattern**: `map/`
-   **View Function**: `main_app.views.sighting_map_view`
-   **Name**: `map_view`
-   **Decorator**: `@login_required` (ensures only authenticated users can access this view).

### View Logic (`main_app.views.sighting_map_view`)

The view function performs the following steps:

1.  **Authentication Check**: Due to the `@login_required` decorator, if the user is not authenticated, they are redirected to the login page.
2.  **Fetch Sightings**: Retrieves all `Sighting` objects from the database using `Sighting.objects.all()`.
3.  **Prepare Sighting Data**: Initializes an empty list called `sightings_data`.
    *   Iterates through each `sighting` object retrieved:
        *   Generates a `detail_url` for the sighting's detail page using `django.urls.reverse('main_app:sighting_detail', args=[sighting.id])`. A fallback to a manually constructed URL (`f'/sighting/{sighting.id}/')` is included in case of an error with `reverse`.
        *   Processes `sighting.image_urls`: If it's a string, it's split by newline characters (`'\n'`) to create a list of URLs. If it's not a string (e.g., already a list), it's used as is.
        *   A dictionary containing relevant details for the map display is created and appended to `sightings_data`. This includes:
            *   `id`: The sighting's ID.
            *   `species_name`: The name of the species.
            *   `description`: A truncated version of the sighting description (first 75 characters followed by "...").
            *   `latitude`: The sighting's latitude.
            *   `longitude`: The sighting's longitude.
            *   `detail_url`: The URL to the sighting's detail page.
            *   `is_native`: Boolean indicating if the species is native.
            *   `image_urls`: A list of image URLs associated with the sighting.
4.  **Prepare Context**: A context dictionary is created for the template:
    *   `mapbox_access_token`: Contains a Mapbox access token. **Note:** This token is currently hardcoded in the view, which is not ideal for security and configuration management. It should be moved to the project's settings.
    *   `sightings_json`: The `sightings_data` list is serialized into a JSON string using `json.dumps()`.
5.  **Render Template**: The `main_app/map_view.html` template is rendered with the prepared `context` and returned as an HTTP response.

### Associated Models

-   `main_app.models.Sighting`: This model is the primary source of data. The view queries all instances of this model.

### Templates Used

-   `main_app/map_view.html`: This template is responsible for displaying the map and embedding the sightings data for use by frontend JavaScript.

## Technical Details

-   The feature relies heavily on a client-side mapping library (indicated by Mapbox usage) to render the interactive map.
-   Data transfer to the frontend is efficiently handled by serializing Python objects (list of dictionaries) into JSON.
-   The use of `django.urls.reverse` for generating detail URLs is a good practice, promoting maintainable URL structures.
-   **Security/Configuration Concern**: The `mapbox_access_token` is hardcoded directly in the view function. Best practice dictates that such sensitive tokens or configuration variables should be stored in `settings.py` (and ideally sourced from environment variables or a secrets management system) and accessed via `from django.conf import settings`.

*(Further technical specifics, if any)* 