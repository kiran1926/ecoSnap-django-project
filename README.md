# ecoSnap Django Project

## Overview

ecoSnap is a web application built with Django that allows users to log, view, and manage sightings of flora and fauna. Users can record observations, view them on an interactive map, and get AI-powered analysis for plant images.

## Features

The application includes the following key features:

-   **[Index Page](./documentation/index_page.md)**: Landing page that directs authenticated users to the map and new users to sign up/login.
-   **[User Signup](./documentation/user_signup.md)**: Allows new users to register for an account.
-   **[Sighting Map View](./documentation/sighting_map_view.md)**: Displays all sightings on an interactive map for authenticated users.
-   **[Sighting Detail View](./documentation/sighting_detail_view.md)**: Shows detailed information for a single sighting.
-   **[Sighting Creation](./documentation/sighting_creation.md)**: Allows authenticated users to add new sightings, including location, description, and images.
-   **[Sighting Update](./documentation/sighting_update.md)**: Enables users to edit their existing sightings.
-   **[Sighting Deletion](./documentation/sighting_deletion.md)**: Allows users to delete their own sightings after confirmation.
-   **[Image Analysis API](./documentation/image_analysis_api.md)**: An API endpoint that uses OpenAI's Vision API to analyze plant images and return information like species name, description, and native status.

For detailed information on each feature, please refer to the linked documentation files.

## Technology Stack

-   **Backend**: Python, Django
-   **Frontend**: HTML, CSS, JavaScript (presumed, for map interaction and API calls)
-   **Database**: SQLite (default, can be configured)
-   **APIs**:
    -   Mapbox (for interactive maps)
    -   OpenAI GPT-4o Vision API (for image analysis)
-   **Other Libraries**: `requests` (for making HTTP requests to OpenAI)

