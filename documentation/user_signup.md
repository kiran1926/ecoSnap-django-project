# User Signup Feature

## Overview

This document describes the User Signup feature, allowing new users to register for an account within the ecoSnap application.

## Frontend Flow

1.  User navigates to the signup page, typically via a link or by accessing the `/signup/` URL directly.
2.  The `registration/signup.html` template is rendered, presenting a registration form to the user.
3.  User fills in the required details (e.g., username, password, password confirmation) and submits the form.
4.  The browser sends a POST request to the `/signup/` URL.
5.  **On successful registration**:
    *   A new user account is created.
    *   The user is automatically logged in.
    *   The user is redirected to the application's index page (`/`). (Which, if they are now authenticated, will further redirect to the map view).
6.  **If registration fails** (e.g., username already exists, passwords do not match, other validation errors):
    *   The signup form is re-displayed.
    *   An error message (e.g., "Invalid sign up - try again") is shown to the user.

## Backend Processing

### URL Pattern

-   **Pattern**: `signup/`
-   **View Function**: `main_app.views.signup`
-   **Name**: `signup`

### View Logic (`main_app.views.signup`)

The `signup` view handles both the display of the registration form (GET request) and the processing of the submitted form data (POST request).

1.  Initializes an `error_message` string to be empty.
2.  **If the request method is `POST`**:
    *   An instance of `django.contrib.auth.forms.UserCreationForm` is created and populated with the submitted data (`request.POST`).
    *   The form's validity is checked using `form.is_valid()`.
        *   **If the form is valid**: 
            *   A new user object is created in the database by calling `user = form.save()`.
            *   The newly created user is logged into the session using `django.contrib.auth.login(request, user)`.
            *   The user is redirected to the URL named `'main_app:index'`.
        *   **If the form is invalid**: 
            *   The `error_message` is set to 'Invalid sign up - try again'.
3.  **If the request method is `GET` (or if a POST request resulted in an invalid form)**:
    *   A new, unbound instance of `UserCreationForm` is created.
4.  A context dictionary is prepared, containing the `form` instance (either newly created or with validation errors) and the `error_message`.
5.  The `registration/signup.html` template is rendered with this context and returned as an HTTP response.

### Associated Forms & Models

-   **Form**: `django.contrib.auth.forms.UserCreationForm`
    *   Handles the validation and creation of new user accounts based on Django's authentication system.
-   **Model**: `django.contrib.auth.models.User` (or a custom user model, if one is configured in `settings.AUTH_USER_MODEL`)
    *   The user data is stored in the table corresponding to this model.

### Templates Used

-   `registration/signup.html`: This template is responsible for rendering the user registration form and displaying any error messages.

## Technical Details

-   Utilizes Django's built-in `UserCreationForm` for robust and secure user registration, handling common tasks like password hashing and validation.
-   The `login()` function integrates with Django's authentication backend to establish a session for the newly registered user.
-   Redirection after successful signup provides a smooth user experience. 