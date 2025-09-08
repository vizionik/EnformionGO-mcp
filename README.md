
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

## Quickstart Guide

This guide will help you get the EnformionGO API wrapper up and running. You can either use Docker (recommended for production) or run it locally for development.

### Prerequisites

*   Python 3.13+
*   `uv` for dependency management (if running locally)
*   Docker (if using Docker)
*   EnformionGO API credentials

### 1. Configure Credentials

Create a `.env` file in the root of the project and add your EnformionGO API credentials:

```
GALAXY_AP_NAME=your_api_name
GALAXY_AP_PASSWORD=your_api_password
```

### 2. Run the Application

You have two options for running the application:

#### Docker (Recommended)

This is the recommended method for a stable deployment.

1.  **Build the Docker image:**
    ```bash
    docker build -t enformiongo .
    ```
2.  **Run the container:**
    ```bash
    docker run -p 8000:8000 --env-file .env enformiongo
    ```

#### Local Development

This method is ideal for development and testing.

1.  **Install dependencies:**
    ```bash
    uv pip sync
    ```
2.  **Run the server with auto-reload:**
    ```bash
    uvicorn main:app --reload
    ```

### 3. Access the API

The application will be accessible at `http://localhost:8000`.

You can view the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

## Usage

Once the application is running, you can connect to it from your client application. The API is available at `http://127.0.0.1:8000` by default.

You can also access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## MCP Server

This application also includes an MCP server. You can find the MCP server at `http://127.0.0.1:8000/mcp`.
