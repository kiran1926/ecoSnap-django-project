# Image Analysis API Feature

## Overview

This document describes the Image Analysis API endpoint located at `/api/analyze-image/`. This API is designed to take a URL of an image, submit it to OpenAI's GPT-4o Vision API for analysis (specifically for plant identification and related information), and then return the structured JSON response obtained from OpenAI.

## Client-Side Interaction (Assumed Frontend Flow)

1.  The client-side application (e.g., JavaScript running in the browser, perhaps during the sighting creation or editing process) obtains a URL for an image. This URL might come from a file upload service like Supabase, as hinted in other parts of the application.
2.  The client makes an asynchronous POST request to the `/api/analyze-image/` endpoint of the Django application.
3.  The body of this POST request must be in JSON format and include an `'image_url'` key. For example:
    ```json
    {
        "image_url": "https://example.com/path/to/plant_image.jpg"
    }
    ```
4.  **Upon successful analysis by the API**:
    *   The Django API responds with a `JsonResponse`. The content of this JSON is the structured data returned by the OpenAI API, typically including fields like `species_name`, `description`, `is_native` (boolean for North America), and `fun_facts`.
    *   If the OpenAI API determines the image is not a plant, the JSON response might contain an `error` field as per the prompt, e.g., `{"error": "Image does not appear to be a plant."}`.
    *   The client-side JavaScript can then parse this JSON response and use the data to auto-fill form fields, display information to the user, or for other relevant actions.
5.  **If the API request encounters an error** (e.g., the `image_url` is missing in the request, an error occurs while communicating with the OpenAI API, or the response from OpenAI cannot be parsed):
    *   The Django API responds with a `JsonResponse` containing an `'error'` key and an appropriate HTTP status code (e.g., 400 for client errors, 500 for server-side or OpenAI API issues).
    *   The client-side JavaScript should be prepared to handle these error responses gracefully.

## Backend Processing

### URL Pattern

-   **Pattern**: `api/analyze-image/`
-   **View Function**: `main_app.views.analyze_image`
-   **Name**: `analyze_image`
-   **Decorators**:
    *   `@require_POST`: Ensures that this view can only be accessed via HTTP POST requests.
    *   `@csrf_exempt`: Disables Django's Cross-Site Request Forgery protection for this view. This is often done for APIs intended for programmatic access, but requires careful consideration of security implications.

### View Logic (`main_app.views.analyze_image`)

The view function processes incoming POST requests as follows:

1.  **Parse Request Body**: It attempts to load the `request.body` as JSON into a Python dictionary (`data`).
2.  **Validate Input**: Checks if `data.get('image_url')` exists. If not, returns a `JsonResponse` with an error message and HTTP status 400.
3.  **OpenAI API Interaction**:
    *   **Security Alert**: An `openai_api_key` is **hardcoded directly in the view function**. This is a critical security vulnerability. API keys should be stored securely (e.g., in environment variables or a Django settings file) and not committed to version control.
    *   Sets up `headers` for the OpenAI API request, including `Content-Type` and the `Authorization` bearer token (the hardcoded API key).
    *   Constructs a `payload` for the OpenAI API (`model: "gpt-4o"`). The payload includes a detailed prompt instructing OpenAI to analyze the plant image and return specific information in JSON format: `species_name`, `description`, `is_native` (to North America), and `fun_facts`. It also asks OpenAI to return an error message if the image is not a plant.
    *   Makes a POST request to the OpenAI Chat Completions endpoint (`https://api.openai.com/v1/chat/completions`) using the `requests` library.
4.  **Handle OpenAI Response**:
    *   If the `response.status_code` from OpenAI is not 200, it returns a `JsonResponse` with an error message (including OpenAI's response text) and HTTP status 500.
    *   If successful (status 200), it parses the JSON response from OpenAI (`result = response.json()`).
    *   Extracts the AI-generated message content: `content = result['choices'][0]['message']['content']`.
5.  **Parse OpenAI Content as JSON**:
    *   It first attempts to parse `content` directly using `json.loads(content)` if the string `content.strip()` starts with `'{'`. 
    *   If direct parsing fails or the content doesn't start with `'{'`, it uses a regular expression (`re.search(r'```json\s*([\s\S]*?)\s*```|{[\s\S]*}', content)`) to find and extract a JSON string that might be embedded within markdown backticks (e.g., ` ```json ... ``` `) or as a raw JSON object string.
    *   If a JSON string is successfully extracted by regex, it's parsed using `json.loads()`.
    *   If JSON parsing fails at any stage, a `JsonResponse` with an error and HTTP status 500 is returned.
6.  **Return Analysis Data**: 
    *   Checks if the parsed `analysis_data` from OpenAI contains an `'error'` key (as per the prompt for non-plant images). If so, returns this error with HTTP status 400.
    *   Otherwise, returns the `analysis_data` as a `JsonResponse` with a default HTTP status 200.
7.  **General Error Handling**: A broad `try...except Exception` block catches any other unexpected errors during the process and returns a `JsonResponse` with a generic error message and HTTP status 500.

### External Services

-   **OpenAI GPT-4o Vision API**: Used for the actual image analysis and information extraction.

### Request Format (to this Django API)

-   **Method**: `POST`
-   **Headers**: `Content-Type: application/json`
-   **Body**: JSON object, e.g., `{"image_url": "<URL_OF_IMAGE_TO_ANALYZE>"}`

### Response Format (from this Django API)

-   **Success (Plant Identified)**: `JsonResponse` with HTTP 200. Body is a JSON object from OpenAI, e.g.:
    ```json
    {
        "species_name": "Quercus robur",
        "description": "A large deciduous tree, native to most of Europe west of the Caucasus.",
        "is_native": false, 
        "fun_facts": "Oak trees can live for over 1000 years."
    }
    ```
-   **Success (Not a Plant or OpenAI-specific error in content)**: `JsonResponse` with HTTP 400. Body is JSON, e.g.:
    ```json
    {"error": "The image does not appear to be a plant."}
    ```
-   **Error (Client-side, e.g., missing `image_url`)**: `JsonResponse` with HTTP 400. Body is JSON, e.g.:
    ```json
    {"error": "No image URL provided"}
    ```
-   **Error (Server-side or OpenAI API communication failure)**: `JsonResponse` with HTTP 500. Body is JSON, e.g.:
    ```json
    {"error": "OpenAI API error: <details>"}
    ```
    or
    ```json
    {"error": "Failed to parse API response as JSON: <details>"}
    ```

## Technical Details & Considerations

-   The `@csrf_exempt` decorator disables CSRF protection. If this API is intended to be called by JavaScript from pages served by the same Django application, it's generally recommended to configure AJAX requests to include the CSRF token rather than exempting the view, to maintain CSRF protection.
-   **Critical Security Vulnerability**: The OpenAI API key is hardcoded directly within the `analyze_image` view function. This key should be immediately removed from the code, stored securely (e.g., as an environment variable or in Django settings loaded from such a variable), and the repository should be checked for any commit history containing the key.
-   The view includes robust error handling for various stages: input validation, OpenAI API communication, and JSON parsing of the OpenAI response.
-   It uses a specific prompt to guide the OpenAI model to return data in a structured JSON format, which is a good practice for reliable data extraction from LLMs.
-   The regex used for parsing JSON from the OpenAI response is a practical approach to handle cases where the LLM might wrap the JSON in markdown or return it with slight variations.

## Frontend Flow (Client-Side Interaction)

1.  A client (e.g., JavaScript in the web application, possibly during sighting creation/editing) has an image URL (e.g., obtained after uploading an image to a service like Supabase).
2.  The client makes an asynchronous POST request to the `/api/analyze-image/` endpoint.
3.  The request body must be JSON and contain an `'image_url'` key with the URL of the image to be analyzed.
    ```json
    {
        "image_url": "http://example.com/path/to/image.jpg"
    }
    ```
4.  **On successful analysis**:
    *   The API responds with a JSON object containing the analysis results (species name, description, native status, fun facts) or an error message if the image is not a plant.
    *   The client-side JavaScript can then use this data to auto-populate form fields, display information to the user, etc.
5.  **If the API request fails** (e.g., no image URL provided, OpenAI API error, JSON parsing error):
    *   The API responds with a JSON error message and an appropriate HTTP status code (400 or 500).
    *   The client-side JavaScript should handle these errors gracefully.

## Backend Processing

### URL Pattern

-   **Pattern**: `api/analyze-image/`
-   **View Function**: `main_app.views.analyze_image`
-   **Name**: `analyze_image`
-   **Decorators**: `@require_POST`, `@csrf_exempt`

### View Logic (`main_app.views.analyze_image`)

*(Details to be filled in based on views.py)*

### External Services

-   OpenAI GPT-4 Vision API

### Request Format (to this API)

-   Method: POST
-   Body: JSON, e.g., `{"image_url": "<URL_TO_IMAGE>"}`

### Response Format (from this API)

-   Success: JSON (structure depends on OpenAI response, typically `{"species_name": "...", "description": "...", "is_native": true/false, "fun_facts": "..."}`)
-   Error: JSON, e.g., `{"error": "<error_message>"}`

## Technical Details

-   `@csrf_exempt` is used, which is common for APIs intended to be called by non-browser clients or via AJAX where CSRF tokens might not be straightforwardly available. However, for AJAX calls from the same origin, CSRF protection should ideally be maintained.
-   **Security Concern**: OpenAI API key is hardcoded directly in the view. This is a major security risk and should be moved to environment variables/settings.
-   Error handling for OpenAI API responses and JSON parsing is present.
-   Specific prompt to OpenAI for structured JSON output.
*(Further technical specifics, if any)* 