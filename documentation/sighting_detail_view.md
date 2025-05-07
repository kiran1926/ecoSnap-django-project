# Sighting Detail View Feature

## Overview

This document describes the Sighting Detail View, which displays comprehensive information about a single, specific sighting. Access to this feature requires user authentication.

## Frontend Flow

1.  An authenticated user navigates to a URL of the format `/sighting/<sighting_id>/`, where `<sighting_id>` is the unique identifier of a specific sighting. This navigation typically occurs by clicking on a marker on the Sighting Map View or a link from another part of the application.
2.  The backend processes the request and renders the `main_app/sighting_detail.html` template.
3.  The rendered page displays detailed information about the requested sighting. This typically includes:
    *   Species name
    *   Full description
    *   Location (latitude, longitude, possibly shown on a static map image)
    *   Any associated images
    *   The user who reported the sighting
    *   Date and time of the sighting
    *   Native status
    *   Other relevant fields from the `Sighting` model.
4.  The page may also include action buttons, such as "Edit" or "Delete," if the currently logged-in user is the owner of the sighting (this logic is typically handled within the template or by separate views).

## Backend Processing

### URL Pattern

-   **Pattern**: `sighting/<int:sighting_id>/`
    *   This pattern captures an integer from the URL path and passes it as `sighting_id` to the view.
-   **View Function**: `main_app.views.sighting_detail_view`
-   **Name**: `sighting_detail`
-   **Decorator**: `@login_required` (ensures only authenticated users can access).

### View Logic (`main_app.views.sighting_detail_view`)

The view function is responsible for fetching and displaying a single sighting:

1.  **Authentication Check**: The `@login_required` decorator ensures that if the user is not logged in, they are redirected to the login page.
2.  **Receive Sighting ID**: The view accepts `request` and `sighting_id` (extracted from the URL) as parameters.
3.  **Fetch Sighting Object**: It attempts to retrieve a `Sighting` instance from the database that matches the provided `sighting_id` using `sighting = get_object_or_404(Sighting, id=sighting_id)`.
    *   If a `Sighting` with the given `id` is found, it is assigned to the `sighting` variable.
    *   If no such `Sighting` exists, `get_object_or_404` automatically raises an `Http404` exception, leading to a "Page Not Found" error being displayed to the user.
4.  **Prepare Context**: A context dictionary is created: `context = {'sighting': sighting}`. This makes the retrieved `sighting` object available to the template.
5.  **Render Template**: The `main_app/sighting_detail.html` template is rendered with the `context` and the resulting HTML is returned as an HTTP response.

### Associated Models

-   `main_app.models.Sighting`: The view directly queries this model to fetch the specific sighting instance.

### Templates Used

-   `main_app/sighting_detail.html`: This template is responsible for presenting all the details of the `sighting` object passed in its context.

## Technical Details

-   Uses Django's `get_object_or_404` shortcut for a common pattern of retrieving an object or returning a 404 error if not found, which is concise and follows best practices.
-   The view is focused and performs a single responsibility: displaying a sighting's details.
-   The actual fields displayed and their formatting are determined by the `main_app/sighting_detail.html` template. 