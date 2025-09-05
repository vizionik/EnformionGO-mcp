
# EnformionGO API Wrapper

This project is a simple FastAPI wrapper for the EnformionGO Person Search and Reverse Phone Search APIs. It provides a convenient way to interact with the EnformionGO API without having to handle the authentication and request signing yourself.

## Capabilities

*   **Person Search:** Search for people by name, address, phone number, and other criteria.
*   **Reverse Phone Search:** Search for people by phone number.
*   **Authentication:** Handles authentication with the EnformionGO API using your API credentials.
*   **Request Validation:** Uses Pydantic models to validate request bodies.

## Limitations

*   **No Database:** This is a pure proxy service and does not have its own database or data persistence layer.
*   **Basic Error Handling:** The API returns basic HTTP exceptions with details from the upstream API or the HTTP client.

## Deployment

To deploy this application, you will need to have Python 3.13+ and the following libraries installed:

```bash
pip install fastapi-mcp fastapi "uvicorn[standard]" httpx python-dotenv
```

You will also need to create a `.env` file in the root of the project with the following content:

```
GALAXY_AP_NAME=
GALAXY_AP_PASSWORD=
```

Once you have created the `.env` file, you can run the application with the following command:

```bash
uvicorn main:app --reload
```

## Connecting a Client

Once the application is running, you can connect to it from your client application. The API is available at `http://127.0.0.1:8000` by default.

You can also access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## MCP Server

This application also includes an MCP server. You can find the MCP server at `http://127.0.0.1:8000/mcp`.
