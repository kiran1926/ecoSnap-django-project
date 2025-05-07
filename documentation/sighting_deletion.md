# Sighting Deletion Feature

## Overview

This document describes the Sighting Deletion feature, which enables authenticated users to remove sightings they have previously created. The process includes a confirmation step to prevent accidental data loss.

## Frontend Flow

1.  An authenticated user initiates the deletion of one of their sightings, usually by clicking a "Delete" button or link available on the Sighting Detail View (`/sighting/<sighting_id>/`) or potentially an Edit Sighting page.
2.  This action navigates the user to the delete confirmation page: `/sighting/<sighting_id>/delete/`.
3.  If the user is not the owner of the sighting, they are redirected (e.g., back to the Sighting Detail View), and the confirmation page is not displayed.
4.  For the owner, the `main_app/sighting_confirm_delete.html` template is rendered. This page typically displays some information about the sighting to be deleted (e.g., species name, date) and asks for explicit confirmation.
5.  The user is presented with options, usually a "Confirm Delete" button (which triggers a POST request) and a "Cancel" button (which might navigate back to the detail page or previous page).
6.  **If the user confirms deletion** (by submitting the form, typically via POST):
    *   The sighting record is permanently removed from the database.
    *   The user is then redirected to a relevant page, such as the Sighting Map View (`/map/`).
7.  **If the user cancels**: They are taken away from the confirmation page, often back to the Sighting Detail View, and no deletion occurs.

## Backend Processing

### URL Pattern

-   **Pattern**: `sighting/<int:sighting_id>/delete/`
-   **View Function**: `main_app.views.sighting_delete_view`
-   **Name**: `sighting_delete`
-   **Decorator**: `@login_required` (ensures only authenticated users can access).

### View Logic (`main_app.views.sighting_delete_view`)

The view handles both the display of the confirmation page (GET) and the actual deletion (POST):

1.  **Authentication & Authorization**:
    *   The `@login_required` decorator ensures the user is logged in.
    *   The `Sighting` object is fetched using `sighting = get_object_or_404(Sighting, id=sighting_id)`.
    *   An ownership check `if request.user != sighting.user:` is performed. If the logged-in user is not the owner of the sighting, they are redirected to the `'main_app:sighting_detail'` page for that sighting, preventing unauthorized deletion.
2.  **If `request.method` is `POST`** (user has confirmed the deletion):
    *   `sighting.delete()` is called. This removes the `Sighting` record from the database.
    *   The user is then redirected to the URL named `'main_app:map_view'`.
3.  **If `request.method` is `GET`** (user is viewing the confirmation page):
    *   A context dictionary `context = {'sighting': sighting}` is prepared, making the `sighting` object available to the template.
    *   The `main_app/sighting_confirm_delete.html` template is rendered with this context.

### Associated Models

-   `main_app.models.Sighting`: The specific instance of this model is fetched and, upon POST confirmation, deleted.
-   `django.contrib.auth.models.User`: Used to verify that `request.user` is the owner (`sighting.user`).

### Templates Used

-   `main_app/sighting_confirm_delete.html`: This template is responsible for displaying the confirmation message and providing the form/button to trigger the POST request for actual deletion.

## Technical Details

-   Employs a crucial ownership check to ensure data integrity and prevent users from deleting others' sightings.
-   Follows the common web pattern of using a GET request to show a confirmation page and a POST request to execute the destructive action (deletion).
-   Uses `get_object_or_404` to gracefully handle cases where a sighting ID in the URL does not correspond to an existing record.
*(Further technical specifics, if any)* 