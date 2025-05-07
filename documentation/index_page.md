# Index Page Feature

## Overview

This document describes the Index Page feature of the ecoSnap application, which serves as the landing page.

## Frontend Flow

1.  User navigates to the root URL (`/`).
2.  **If the user is authenticated**: They are redirected to the Sighting Map View (`/map/`).
3.  **If the user is not authenticated**: The `main_app/index.html` template is rendered and displayed to the user.

## Backend Processing

### URL Pattern

-   **Pattern**: `''` (root path)
-   **View Function**: `main_app.views.index`
-   **Name**: `index`

### View Logic (`main_app.views.index`)

The `index` view function performs the following:

1.  Checks if the current `request.user` is authenticated using `request.user.is_authenticated`.
2.  **If authenticated**: It issues an HTTP redirect (302 Found) to the URL corresponding to the `'main_app:map_view'` named URL pattern. This typically directs the user to the main map interface of the application.
3.  **If not authenticated**: It renders the `main_app/index.html` template. This template likely serves as a welcome page, possibly with options to sign up or log in.

### Associated Models

-   Implicitly interacts with `django.contrib.auth.models.User` (or a custom user model if configured) via `request.user.is_authenticated`.
-   No direct database queries for custom application models are performed by this view for its primary logic.

### Templates Used

-   `main_app/index.html`: Rendered for unauthenticated users.

## Technical Details

-   The redirection for authenticated users enhances user experience by taking them directly to the application's core functionality.
-   Serves as a clear entry point, differentiating experiences for logged-in versus anonymous users. 