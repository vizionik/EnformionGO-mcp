
# EnformionGO API Wrapper

This project is a FastAPI wrapper for a wide range of EnformionGO API endpoints. It simplifies interaction with the EnformionGO API by handling authentication and providing validated request models. It also exposes the API as an MCP-enabled server using `fastapi-mcp`.

## Capabilities

This wrapper provides access to the following categories of EnformionGO APIs:

*   **Dev APIs (Single Result):**
    *   Contact Enrichment: Find more data about a contact.
    *   Caller ID: Get information for a phone number.
    *   Email ID: Get information for an email address.
    *   Contact ID: Search for contact info by person ID.
    *   Address ID: Find contact info for property owners/residents.
    *   Address AutoComplete: Autocomplete addresses.
*   **People Data:**
    *   Person Search: Comprehensive search for people.
    *   Reverse Phone Search: Find people associated with a phone number.
    *   ID Verification: Verify an identity and get a score.
    *   Census Search: Search historical population data.
    *   Divorce Search: Search for divorce records.
    *   LinkedIn ID: Search using a LinkedIn profile URL.
*   **Property Data:**
    *   Property Search V2: Search for property data.
*   **Business Data:**
    *   Business Search: Search for business information.
    *   Domain Search: Search for domain data.
    *   Workplace Search: Search for workplace data.
    *   Business ID: Search by business ID.

It also features:
*   **Authentication:** Handles authentication with the EnformionGO API using your API credentials.
*   **Request Validation:** Uses Pydantic models to validate request bodies.
*   **MCP Server:** Exposes the API as an MCP server.

## Limitations

*   **Bring Your Own Key:** You must have your own EnformionGO API credentials.
*   **No Database:** This is a pure proxy service and does not have its own database or data persistence layer.
*   **Basic Error Handling:** The API returns basic HTTP exceptions with details from the upstream API or the HTTP client.
*   **Undefined Schemas:** Some newer endpoints (`property-search-v2`, `domain-search`, `business-id`) do not have Pydantic models defined and accept a generic JSON body.

## Setup and Running

This application can be run either using Docker (recommended) or directly on your local machine for development. In both cases, you first need to create an environment file.

1.  **Create Environment File:**

    Create a `.env` file in the root of the project with your EnformionGO API credentials:
    ```
    GALAXY_AP_NAME=your_api_name
    GALAXY_AP_PASSWORD=your_api_password
    ```

### Running with Docker (Recommended)

The `Dockerfile` included in the project provides a production-ready environment using `gunicorn`. This is the simplest and recommended way to run the application.

1.  **Prerequisites:**
    *   Ensure you have Docker installed on your system.

2.  **Build and Run the Docker Container:**
    From the root of the project, run the following commands:

    ```bash
    # Build the Docker image
    docker build -t enformiongo .

    # Run the container, passing the .env file for credentials
    docker run -p 8000:8000 --env-file .env enformiongo
    ```

    The application will be accessible at `http://localhost:8000`.

### Running Locally for Development

For development purposes, you can run the application directly on your machine. You will need Python 3.13+ and `uv` for dependency management.

1.  **Install `uv`:**
    If you don't have `uv`, install it via `pip` or your preferred method:
    ```bash
    pip install uv
    ```
2.  **Install Dependencies:**
    Sync the dependencies from the `uv.lock` file:
    ```bash
    uv pip sync
    ```
3.  **Run the Application:**
    You can run the application with `uvicorn` which provides live reloading, ideal for development:
    ```bash
    uvicorn main:app --reload
    ```

## Usage

Once the application is running, you can connect to it from your client application. The API is available at `http://127.0.0.1:8000` by default.

You can also access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## MCP Server

This application also includes an MCP server. You can find the MCP server at `http://127.0.0.1:8000/mcp`.
