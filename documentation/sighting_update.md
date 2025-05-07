# Sighting Update Feature

## Overview

This document describes the Sighting Update feature, which allows authenticated users to modify the details of sightings they have previously created. It utilizes the same form and template as the sighting creation process but is pre-populated with the existing data of the sighting being edited.

## Frontend Flow

1.  An authenticated user navigates to the edit page for one of their sightings. This is typically achieved by clicking an "Edit" button or link on the Sighting Detail View page (`/sighting/<sighting_id>/`). The URL for editing is `/sighting/<sighting_id>/edit/`.
2.  If the user is not the owner of the sighting, they are redirected away (e.g., back to the Sighting Detail View), and the edit form is not displayed.
3.  For the owner, the `main_app/sighting_form.html` template is rendered. The form fields are pre-filled with the current data of the sighting being edited.
4.  The user modifies the desired fields in the form (e.g., species name, description, location via map, images, native status).
5.  The user submits the form.
6.  The browser sends a POST request to `/sighting/<sighting_id>/edit/` with the updated form data.
7.  **On successful update**:
    *   The corresponding `Sighting` record in the database is updated with the new information.
    *   The user is redirected to the Sighting Detail View (`/sighting/<sighting_id>/`) for the now-updated sighting.
8.  **If form submission fails** (due to validation errors):
    *   The `main_app/sighting_form.html` template is re-rendered.
    *   The form is pre-filled with the data the user attempted to submit (including their modifications).
    *   Error messages are displayed to guide the user in correcting the input.

## Backend Processing

### URL Pattern

-   **Pattern**: `sighting/<int:sighting_id>/edit/`
-   **View Function**: `main_app.views.sighting_update_view`
-   **Name**: `sighting_edit`
-   **Decorator**: `@login_required` (ensures only authenticated users can access).

### View Logic (`main_app.views.sighting_update_view`)

The view handles fetching the existing sighting, displaying the form for editing, and processing the submitted updates:

1.  **Authentication & Authorization**: The `@login_required` decorator ensures the user is logged in.
    *   The view retrieves the `Sighting` object using `sighting = get_object_or_404(Sighting, id=sighting_id)`.
    *   It then checks if `request.user == sighting.user`. If the current user is not the owner of the sighting, they are redirected to the `'main_app:sighting_detail'` page for that sighting (preventing unauthorized edits).
2.  **If `request.method` is `POST`** (form submission with updated data):
    *   An instance of `main_app.forms.SightingForm` is created, populated with the submitted data (`request.POST`) and bound to the existing `sighting` instance (`instance=sighting`).
    *   The form's validity is checked using `form.is_valid()`.
        *   **If valid**: `form.save()` is called, which updates the existing `sighting` record in the database with the new data. The user is then redirected to the `'main_app:sighting_detail'` URL for the `sighting.id`.
        *   **If invalid**: The form instance (containing error information and the user's submitted data) proceeds to be rendered in the template.
3.  **If `request.method` is `GET`** (initial display of the edit form or re-display after POST with errors):
    *   If it's a GET request, `form = SightingForm(instance=sighting)` creates a form instance pre-populated with the data from the `sighting` object.
    *   If it's a POST request that failed validation, the bound form from the POST handling is used.
4.  **Prepare Context**: A context dictionary is created:
    *   `'form'`: The `SightingForm` instance (bound to the `sighting` object, pre-filled with its data, and potentially containing validation errors if a POST failed).
    *   `'sighting'`: The original `sighting` object (can be used in the template, e.g., for page titles like "Editing Sighting [Species Name]").
    *   `'edit_mode'`: Set to `True`. This boolean flag can be used by the `sighting_form.html` template to slightly alter its presentation or behavior for editing (e.g., changing button text from "Create" to "Save Changes").
    *   `'mapbox_access_token'`: A hardcoded Mapbox access token. (Same concern as previous views: should be in settings).
5.  **Render Template**: The `main_app/sighting_form.html` template is rendered with this context.

### Associated Forms & Models

-   **Form**: `main_app.forms.SightingForm` (reused from the creation feature)
    *   When instantiated with `instance=sighting`, it pre-populates with the sighting's data and, upon saving, updates that specific instance.
-   **Model**: `main_app.models.Sighting`
    *   The specific instance of this model is fetched and updated.
-   **Model**: `django.contrib.auth.models.User`
    *   Used to verify that `request.user` is the owner (`sighting.user`).

### Templates Used

-   `main_app/sighting_form.html`: The same template used for creating sightings. The `edit_mode` context variable can be used within this template to differentiate the user experience (e.g., page title, button labels).

## Technical Details

-   Crucially includes an ownership check (`request.user != sighting.user`) to prevent unauthorized users from editing sightings.
-   Reuses the `SightingForm` and the `sighting_form.html` template, promoting DRY (Don't Repeat Yourself) principles. The `instance` argument to the form constructor is key for this reuse in edit mode.
-   The `edit_mode` boolean passed to the template is a simple way to allow the template to adapt to whether it's being used for creation or editing.
-   The hardcoded Mapbox token remains a point for improvement.
*(Further technical specifics, if any)* 