# Sighting Creation Feature

## Overview

This document describes the Sighting Creation feature, which allows authenticated users to add new sightings to the application. This involves submitting a form with details about the observed species, its location, and optional images.

## Frontend Flow

1.  An authenticated user initiates the creation of a new sighting, typically by clicking an "Add New Sighting" button or link (e.g., from the map view). This navigates them to `/sighting/create/`.
2.  The `main_app/sighting_form.html` template is rendered. This page displays a form for entering sighting details.
3.  The form includes fields for:
    *   **Species Name**: Text input.
    *   **Description**: Text area.
    *   **Location**: Latitude and Longitude fields are present as hidden inputs. These are expected to be populated by client-side JavaScript interacting with an embedded map (e.g., Mapbox) where the user can click or search to set the location.
    *   **Image URLs**: A text area where users can paste image URLs (one per line), presumably after uploading them to an external service like Supabase, as indicated by placeholder text.
    *   **Is Native**: A select dropdown (Yes/No/Unknown).
4.  The user fills out the form details and clicks the submit button.
5.  The browser sends a POST request to `/sighting/create/` with the form data.
6.  **On successful creation**:
    *   A new `Sighting` record is created in the database, associated with the logged-in user.
    *   The user is redirected to the Sighting Detail View for the newly created sighting (e.g., `/sighting/<new_id>/`).
7.  **If form submission fails** (due to validation errors like missing required fields or incorrect data types):
    *   The `main_app/sighting_form.html` template is re-rendered.
    *   The form is pre-filled with the data the user previously entered.
    *   Error messages are displayed next to the problematic fields or at the top of the form, guiding the user to make corrections.

## Backend Processing

### URL Pattern

-   **Pattern**: `sighting/create/`
-   **View Function**: `main_app.views.sighting_create_view`
-   **Name**: `sighting_create`
-   **Decorator**: `@login_required` (ensures only authenticated users can access).

### View Logic (`main_app.views.sighting_create_view`)

The view handles both GET (displaying the form) and POST (processing submitted data) requests:

1.  **Authentication Check**: The `@login_required` decorator redirects non-authenticated users to the login page.
2.  **If `request.method` is `POST`** (form submission):
    *   An instance of `main_app.forms.SightingForm` is created with the submitted data (`request.POST`).
    *   The form's validity is checked using `form.is_valid()`.
        *   **If valid**: 
            *   `new_sighting = form.save(commit=False)`: A `Sighting` model instance is created from the form data but not yet saved to the database. This allows modification before the final save.
            *   `new_sighting.user = request.user`: The `user` field of the new sighting is set to the currently logged-in user.
            *   `new_sighting.save()`: The sighting is saved to the database.
            *   The user is redirected to the `'main_app:sighting_detail'` URL for the `new_sighting.id`.
        *   **If invalid**: The form instance (now containing error information) falls through to be rendered in the template.
3.  **If `request.method` is `GET`** (initial form display or re-display after POST with errors):
    *   An unbound instance of `SightingForm` is created if it's a GET request. If it's a POST request that failed validation, the bound form from the POST handling is used.
4.  **Prepare Context**: A context dictionary is created:
    *   `'form'`: The `SightingForm` instance (either empty, with user data, or with user data and error messages).
    *   `'mapbox_access_token'`: A hardcoded Mapbox access token. **Note:** This should be moved to project settings for better security and configurability.
5.  **Render Template**: The `main_app/sighting_form.html` template is rendered with this context.

### Associated Forms & Models

-   **Form**: `main_app.forms.SightingForm`
    *   A `ModelForm` based on the `Sighting` model.
    *   Defines fields: `species_name` (TextInput), `description` (Textarea), `latitude` (HiddenInput), `longitude` (HiddenInput), `image_urls` (Textarea, optional), `is_native` (Select).
    *   Includes custom widgets, placeholders, and help texts for better user experience.
    *   The `latitude` and `longitude` fields are hidden, implying they are set by JavaScript based on map interaction.
-   **Model**: `main_app.models.Sighting`
    *   The data submitted through the form (once validated) is used to create a new record for this model.
-   **Model**: `django.contrib.auth.models.User` (or custom user model)
    *   The created sighting is associated with the `request.user`.

### Templates Used

-   `main_app/sighting_form.html`: This template renders the sighting creation form and is also used to display validation errors. It likely contains JavaScript for map interaction to set latitude/longitude and to handle image URL input.

## Technical Details

-   The use of `form.save(commit=False)` is a common Django pattern to modify a model instance before saving it, particularly useful here for associating the `request.user`.
-   The Mapbox token hardcoding is a recurring concern and should be addressed by moving it to `settings.py`.
-   The form relies on client-side JavaScript to populate the hidden `latitude` and `longitude` fields, which is a common approach for map-based input.

*(Further technical specifics, if any)* 